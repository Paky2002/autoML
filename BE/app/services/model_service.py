# BE/app/services/model_service.py
from typing import List, Optional, Dict, Any
import logging
import os

from services.base import (
    TrainingConfig, DatasetInfo, TrainingResult, 
    PredictionRequest, PredictionResult, ModelStatus
)
from services.interfaces import IMLService

logger = logging.getLogger(__name__)

class ModelService:
    """Main service for managing machine learning models"""
    
    def __init__(
        self, 
        ml_service: Optional[IMLService] = None,
        model_repository = None  # Use duck typing to avoid circular imports
    ):
        self.ml_service = ml_service
        self.model_repository = model_repository
    
    def train_model(self, dataset: DatasetInfo, config: TrainingConfig) -> Dict[str, Any]:
        """
        Train a new model with the given dataset and configuration
        """
        try:
            logger.info(f"Starting training for model: {config.model_name}")
            
            # Validate inputs
            self._validate_training_inputs(dataset, config)
            
            # Create database record with TRAINING status
            model_record = self.model_repository.create(
                training_config=config,
                model_path="",  # Will be updated after training
                dataset_filename=dataset.filename
            )
            
            try:
                # Perform ML training
                training_result = self.ml_service.train_model(dataset, config)
                
                if training_result.success:
                    # Get the ACTUAL path where AutoGluon saved the model
                    actual_model_path = training_result.model_path
                    
                    # Extract the actual UUID from the path
                    actual_uuid = os.path.basename(actual_model_path)
                    
                    # Update the database record with the ACTUAL UUID and path
                    model_record.uuid = actual_uuid  # Use AutoGluon's UUID
                    model_record.model_path = actual_model_path
                    
                    self.model_repository.update_status(
                        actual_uuid,  # Use the actual UUID
                        ModelStatus.COMPLETED,
                        {
                            'best_score': training_result.best_score,
                            'best_model_name': training_result.best_model_name
                        }
                    )
                    
                    # Return the ACTUAL UUID to the frontend
                    return {
                        'success': True,
                        'model_uuid': actual_uuid,  # This will match the filesystem
                        'model_name': config.model_name,
                        'best_score': training_result.best_score,
                        'best_model_name': training_result.best_model_name,
                        'leaderboard': training_result.leaderboard
                    }
                else:
                    # Update status to FAILED
                    self.model_repository.update_status(
                        model_record.uuid,
                        ModelStatus.FAILED,
                        {'error_message': training_result.error_message}
                    )
                    
                    logger.error(f"Training failed for model: {model_record.uuid}")
                    
                    return {
                        'success': False,
                        'model_uuid': model_record.uuid,
                        'error': training_result.error_message
                    }
                    
            except Exception as e:
                # Update status to FAILED on exception
                self.model_repository.update_status(
                    model_record.uuid,
                    ModelStatus.FAILED,
                    {'error_message': str(e)}
                )
                raise
                
        except Exception as e:
            logger.error(f"Training service error: {str(e)}")
            return {
                'success': False,
                'error': f"Training service error: {str(e)}"
            }
    
    def get_all_models(self) -> List[Dict[str, Any]]:
        """Get all trained models"""
        try:
            models = self.model_repository.get_all()
            return [model.to_dict() for model in models]
        except Exception as e:
            logger.error(f"Error retrieving models: {str(e)}")
            raise
    
    def get_model_by_uuid(self, model_uuid: str) -> Optional[Dict[str, Any]]:
        """Get a specific model by UUID"""
        try:
            model = self.model_repository.get_by_uuid(model_uuid)
            if not model:
                return None
            
            model_dict = model.to_dict()
            
            # Enrich with ML model information if available
            if model.model_path and model.status == ModelStatus.COMPLETED.value:
                ml_info = self.ml_service.get_model_info(model.model_path)
                if ml_info:
                    model_dict.update({
                        'feature_columns': ml_info.get('feature_columns', []),
                        'feature_importance': ml_info.get('feature_importance'),
                        'detailed_leaderboard': ml_info.get('leaderboard')
                    })
            
            return model_dict
            
        except Exception as e:
            logger.error(f"Error retrieving model {model_uuid}: {str(e)}")
            raise
    
    def delete_model(self, model_uuid: str) -> bool:
        """Delete a model (database record and files)"""
        try:
            model = self.model_repository.get_by_uuid(model_uuid)
            if not model:
                return False
            
            # Delete ML model files
            if model.model_path:
                self.ml_service.delete_model(model_uuid)
            
            # Delete database record
            return self.model_repository.delete(model_uuid)
            
        except Exception as e:
            logger.error(f"Error deleting model {model_uuid}: {str(e)}")
            raise
    
    def predict(self, model_uuid: str, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Make predictions using a trained model"""
        try:
            # Validate model exists and is ready
            model = self.model_repository.get_by_uuid(model_uuid)
            if not model:
                return {
                    'success': False,
                    'error': f'Model {model_uuid} not found'
                }
            
            if model.status != ModelStatus.COMPLETED.value:
                return {
                    'success': False,
                    'error': f'Model {model_uuid} is not ready for predictions. Status: {model.status}'
                }
            
            # Create prediction request
            request = PredictionRequest(
                model_uuid=model_uuid,
                data=prediction_data
            )
            
            # Perform prediction
            result = self.ml_service.predict(request)
            
            if result.success:
                logger.info(f"Prediction completed for model: {model_uuid}")
                return {
                    'success': True,
                    'model_uuid': model_uuid,
                    'model_name': model.name,
                    'predictions': result.predictions,
                    'probabilities': result.probabilities,
                    'target_feature': model.target_feature
                }
            else:
                logger.error(f"Prediction failed for model: {model_uuid}")
                return {
                    'success': False,
                    'error': result.error_message
                }
                
        except Exception as e:
            logger.error(f"Prediction service error for model {model_uuid}: {str(e)}")
            return {
                'success': False,
                'error': f"Prediction service error: {str(e)}"
            }
    
    def get_model_status(self, model_uuid: str) -> Optional[str]:
        """Get the current status of a model"""
        try:
            model = self.model_repository.get_by_uuid(model_uuid)
            return model.status if model else None
        except Exception as e:
            logger.error(f"Error getting model status {model_uuid}: {str(e)}")
            return None
    
    def _validate_training_inputs(self, dataset: DatasetInfo, config: TrainingConfig) -> None:
        """Validate training inputs"""
        if not dataset.headers:
            raise ValueError("Dataset must have headers")
        
        if not dataset.rows:
            raise ValueError("Dataset must have data rows")
        
        if config.target_feature not in dataset.headers:
            raise ValueError(f"Target feature '{config.target_feature}' not found in dataset headers")
        
        if config.time_limit <= 0:
            raise ValueError("Time limit must be positive")
        
        if not config.model_name.strip():
            raise ValueError("Model name cannot be empty")