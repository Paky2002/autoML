# BE/app/services/ml_service.py
import os
import pandas as pd
import shutil
from typing import Dict, Any, List, Optional
from pathlib import Path
import uuid
import logging

# Import base classes
from services.base import (
    TrainingConfig, DatasetInfo, TrainingResult, 
    PredictionRequest, PredictionResult, ProblemType
)
from services.interfaces import IMLService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoGluonMLService(IMLService):
    """AutoGluon implementation of ML service"""
    
    def __init__(self, models_base_path: str = "models_output"):
        # Make sure the path is relative to the project root (where run.py is)
        import os
        if not os.path.isabs(models_base_path):
            # Get the directory where run.py is located (project root)
            # Current file is: BE/app/services/ml_service.py
            # We need to go up 3 levels to reach the project root (where run.py is)
            current_file = os.path.abspath(__file__)  # .../BE/app/services/ml_service.py
            app_dir = os.path.dirname(os.path.dirname(current_file))  # .../BE/app
            be_dir = os.path.dirname(app_dir)  # .../BE
            project_root = be_dir  # .../BE (where run.py is)
            models_base_path = os.path.join(project_root, models_base_path)
        
        self.models_base_path = Path(models_base_path)
        self.models_base_path.mkdir(exist_ok=True)
        self._loaded_models: Dict[str, Any] = {}  # Use Any to avoid import issues
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Models base path set to: {self.models_base_path}")
    
    def train_model(self, dataset: DatasetInfo, config: TrainingConfig) -> TrainingResult:
        """Train a model using AutoGluon"""
        try:
            # Import AutoGluon only when needed
            from autogluon.tabular import TabularPredictor
        except ImportError:
            logger.error("AutoGluon not installed. Please install with: pip install autogluon")
            return TrainingResult(
                success=False,
                error_message="AutoGluon not installed. Please install with: pip install autogluon"
            )
        
        model_uuid = str(uuid.uuid4())
        model_dir = self.models_base_path / model_uuid
        
        try:
            # Create model directory
            model_dir.mkdir(exist_ok=True)
            logger.info(f"Starting training for model {model_uuid}")
            logger.info(f"Model will be saved to: {model_dir}")
            
            # Convert data to DataFrame
            df = self._prepare_dataframe(dataset)
            
            # Validate target column
            if config.target_feature not in df.columns:
                raise ValueError(f"Target feature '{config.target_feature}' not found in dataset")
            
            # Configure AutoGluon predictor
            predictor_config = self._build_predictor_config(config, str(model_dir))
            
            # Create and train predictor
            predictor = TabularPredictor(**predictor_config)
            
            # Perform training
            predictor.fit(
                train_data=df,
                time_limit=config.time_limit,
                presets=config.presets,
                verbosity=config.verbosity
            )
            
            # Verify the model was saved
            if not model_dir.exists():
                raise Exception(f"Model directory was not created: {model_dir}")
            
            # Get training results
            leaderboard = predictor.leaderboard(silent=True)
            best_model = leaderboard.iloc[0]
            
            # Cache the trained model
            self._loaded_models[model_uuid] = predictor
            
            logger.info(f"Training completed successfully for model {model_uuid}")
            logger.info(f"Model saved to: {model_dir}")
            
            return TrainingResult(
                success=True,
                model_uuid=model_uuid,
                model_path=str(model_dir),
                best_model_name=str(best_model['model']),
                best_score=float(best_model['score_val']),
                leaderboard=leaderboard.head(5).to_dict('records')
            )
            
        except Exception as e:
            logger.error(f"Training failed for model {model_uuid}: {str(e)}")
            
            # Cleanup on failure
            if model_dir.exists():
                shutil.rmtree(model_dir)
            
            return TrainingResult(
                success=False,
                error_message=f"Training failed: {str(e)}"
            )
    
    def load_model(self, model_path: str) -> bool:
        """Load a trained model"""
        try:
            from autogluon.tabular import TabularPredictor
        except ImportError:
            logger.error("AutoGluon not installed")
            return False
            
        try:
            model_path_obj = Path(model_path)
            logger.info(f"Attempting to load model from: {model_path_obj}")
            
            if not model_path_obj.exists():
                logger.error(f"Model path does not exist: {model_path}")
                # List what's actually in the models directory
                if self.models_base_path.exists():
                    logger.info(f"Available models in {self.models_base_path}:")
                    for item in self.models_base_path.iterdir():
                        logger.info(f"  - {item.name}")
                else:
                    logger.error(f"Models base path does not exist: {self.models_base_path}")
                return False
            
            # Extract model UUID from path
            model_uuid = model_path_obj.name
            
            # Check if already loaded
            if model_uuid in self._loaded_models:
                logger.info(f"Model {model_uuid} already loaded in cache")
                return True
            
            # Load the model
            predictor = TabularPredictor.load(model_path)
            self._loaded_models[model_uuid] = predictor
            
            logger.info(f"Model {model_uuid} loaded successfully from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {str(e)}")
            return False
    
    def predict(self, request: PredictionRequest) -> PredictionResult:
        """Make predictions using a trained model"""
        try:
            # Load model if not cached
            if request.model_uuid not in self._loaded_models:
                model_path = self.models_base_path / request.model_uuid
                if not self.load_model(str(model_path)):
                    return PredictionResult(
                        success=False,
                        error_message=f"Failed to load model {request.model_uuid}"
                    )
            
            predictor = self._loaded_models[request.model_uuid]
            
            # Prepare data for prediction
            df = pd.DataFrame(request.data)
            
            # Make predictions
            predictions = predictor.predict(df)
            
            # Get prediction probabilities if available (for classification)
            probabilities = None
            try:
                if hasattr(predictor, 'predict_proba'):
                    prob_df = predictor.predict_proba(df)
                    probabilities = prob_df.values.tolist()
            except:
                # Probabilities not available (e.g., for regression)
                pass
            
            logger.info(f"Predictions completed for model {request.model_uuid}")
            
            return PredictionResult(
                success=True,
                predictions=predictions.tolist() if hasattr(predictions, 'tolist') else list(predictions),
                probabilities=probabilities
            )
            
        except Exception as e:
            logger.error(f"Prediction failed for model {request.model_uuid}: {str(e)}")
            return PredictionResult(
                success=False,
                error_message=f"Prediction failed: {str(e)}"
            )
    
    def get_model_info(self, model_path: str) -> Optional[Dict[str, Any]]:
        """Get information about a trained model"""
        try:
            model_path_obj = Path(model_path)
            model_uuid = model_path_obj.name
            
            # Load model if not cached
            if model_uuid not in self._loaded_models:
                if not self.load_model(model_path):
                    return None
            
            predictor = self._loaded_models[model_uuid]
            
            # Get model information
            info = {
                'model_uuid': model_uuid,
                'problem_type': predictor.problem_type,
                'label_column': predictor.label,
                'feature_columns': list(predictor.feature_metadata_in.keys()),
                'eval_metric': predictor.eval_metric,
            }
            
            # Get leaderboard if available
            try:
                leaderboard = predictor.leaderboard(silent=True)
                info['leaderboard'] = leaderboard.head(10).to_dict('records')
                info['best_model'] = leaderboard.iloc[0]['model']
                info['best_score'] = float(leaderboard.iloc[0]['score_val'])
            except:
                pass
            
            # Get feature importance if available
            try:
                importance = predictor.feature_importance(data=None, subsample_size=1000)
                info['feature_importance'] = importance.to_dict()
            except:
                pass
            
            return info
            
        except Exception as e:
            logger.error(f"Failed to get model info for {model_path}: {str(e)}")
            return None
    
    def delete_model(self, model_uuid: str) -> bool:
        """Delete model files and remove from cache"""
        try:
            # Remove from cache
            if model_uuid in self._loaded_models:
                del self._loaded_models[model_uuid]
            
            # Delete model directory
            model_path = self.models_base_path / model_uuid
            if model_path.exists():
                shutil.rmtree(model_path)
                logger.info(f"Model {model_uuid} deleted successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete model {model_uuid}: {str(e)}")
            return False
    
    def _prepare_dataframe(self, dataset: DatasetInfo) -> pd.DataFrame:
        """Convert dataset info to pandas DataFrame"""
        df = pd.DataFrame(dataset.rows, columns=dataset.headers)
        
        # Clean column names (remove whitespace)
        df.columns = df.columns.str.strip()
        
        # Basic data cleaning
        df = df.dropna(how='all')  # Remove completely empty rows
        
        return df
    
    def _build_predictor_config(self, config: TrainingConfig, model_path: str) -> Dict[str, Any]:
        """Build AutoGluon predictor configuration"""
        predictor_config = {
            'label': config.target_feature,
            'path': model_path,
            'verbosity': config.verbosity
        }
        
        # Add problem type if specified
        if config.problem_type != ProblemType.AUTO:
            predictor_config['problem_type'] = config.problem_type.value
        
        # Add evaluation metric if specified
        if config.eval_metric:
            predictor_config['eval_metric'] = config.eval_metric
        
        return predictor_config