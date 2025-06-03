# BE/app/services/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from services.base import TrainingConfig, DatasetInfo, TrainingResult, PredictionRequest, PredictionResult

class IMLService(ABC):
    """Interface for ML service"""
    
    @abstractmethod
    def train_model(self, dataset: DatasetInfo, config: TrainingConfig) -> TrainingResult:
        pass
    
    @abstractmethod
    def load_model(self, model_path: str) -> bool:
        pass
    
    @abstractmethod
    def predict(self, request: PredictionRequest) -> PredictionResult:
        pass
    
    @abstractmethod
    def get_model_info(self, model_path: str) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def delete_model(self, model_uuid: str) -> bool:
        pass