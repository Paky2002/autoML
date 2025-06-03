# BE/app/repositories/model_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from models import TrainedModel
from extensions import db
from services.base import TrainingConfig, ModelStatus
import uuid
from datetime import datetime

class IModelRepository(ABC):
    """Interface for model repository"""
    
    @abstractmethod
    def create(self, training_config: TrainingConfig, model_path: str, dataset_filename: str) -> TrainedModel:
        pass
    
    @abstractmethod
    def get_by_uuid(self, model_uuid: str) -> Optional[TrainedModel]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[TrainedModel]:
        pass
    
    @abstractmethod
    def update(self, model: TrainedModel) -> TrainedModel:
        pass
    
    @abstractmethod
    def delete(self, model_uuid: str) -> bool:
        pass
    
    @abstractmethod
    def exists(self, model_uuid: str) -> bool:
        pass

class ModelRepository(IModelRepository):
    """Concrete implementation of model repository"""
    
    def create(self, training_config: TrainingConfig, model_path: str, dataset_filename: str) -> TrainedModel:
        """Create a new trained model record"""
        try:
            model = TrainedModel(
                uuid=str(uuid.uuid4()),
                name=training_config.model_name,
                model_path=model_path,
                target_feature=training_config.target_feature,
                problem_type=training_config.problem_type.value,
                time_limit=training_config.time_limit,
                eval_metric=training_config.eval_metric,
                presets=training_config.presets,
                verbosity=training_config.verbosity,
                dataset_filename=dataset_filename,
                status=ModelStatus.TRAINING.value,
                created_at=datetime.utcnow()
            )
            
            db.session.add(model)
            db.session.commit()
            return model
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to create model record: {str(e)}")
    
    def get_by_uuid(self, model_uuid: str) -> Optional[TrainedModel]:
        """Get model by UUID"""
        return TrainedModel.query.filter_by(uuid=model_uuid).first()
    
    def get_all(self) -> List[TrainedModel]:
        """Get all models ordered by creation date"""
        return TrainedModel.query.order_by(TrainedModel.created_at.desc()).all()
    
    def update(self, model: TrainedModel) -> TrainedModel:
        """Update existing model"""
        try:
            db.session.commit()
            return model
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update model: {str(e)}")
    
    def delete(self, model_uuid: str) -> bool:
        """Delete model by UUID"""
        try:
            model = self.get_by_uuid(model_uuid)
            if not model:
                return False
            
            db.session.delete(model)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to delete model: {str(e)}")
    
    def exists(self, model_uuid: str) -> bool:
        """Check if model exists"""
        return TrainedModel.query.filter_by(uuid=model_uuid).first() is not None
    
    def update_status(self, model_uuid: str, status: ModelStatus, additional_data: dict = None) -> bool:
        """Update model status and additional data"""
        try:
            model = self.get_by_uuid(model_uuid)
            if not model:
                return False
            
            model.status = status.value
            
            if additional_data:
                if 'best_score' in additional_data:
                    model.best_score = additional_data['best_score']
                if 'best_model_name' in additional_data:
                    model.best_model_name = additional_data['best_model_name']
                if 'error_message' in additional_data:
                    model.error_message = additional_data['error_message']
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Failed to update model status: {str(e)}")