# BE/app/services/base.py
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class ModelStatus(Enum):
    TRAINING = "training"
    COMPLETED = "completed"
    FAILED = "failed"
    DELETED = "deleted"

class ProblemType(Enum):
    REGRESSION = "regression"
    BINARY = "binary"
    MULTICLASS = "multiclass"
    AUTO = "auto"

@dataclass
class TrainingConfig:
    """Configuration for model training"""
    model_name: str
    target_feature: str
    problem_type: ProblemType
    time_limit: int = 600
    eval_metric: Optional[str] = None
    presets: str = "best_quality"
    verbosity: int = 2
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_name': self.model_name,
            'target_feature': self.target_feature,
            'problem_type': self.problem_type.value,
            'time_limit': self.time_limit,
            'eval_metric': self.eval_metric,
            'presets': self.presets,
            'verbosity': self.verbosity
        }

@dataclass
class DatasetInfo:
    """Dataset information"""
    filename: str
    headers: List[str]
    rows: List[List[Any]]
    total_rows: int
    file_size: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'filename': self.filename,
            'headers': self.headers,
            'rows': self.rows,
            'total_rows': self.total_rows,
            'file_size': self.file_size
        }

@dataclass
class TrainingResult:
    """Result of model training"""
    success: bool
    model_uuid: Optional[str] = None
    model_path: Optional[str] = None
    best_model_name: Optional[str] = None
    best_score: Optional[float] = None
    leaderboard: Optional[List[Dict]] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'model_uuid': self.model_uuid,
            'model_path': self.model_path,
            'best_model_name': self.best_model_name,
            'best_score': self.best_score,
            'leaderboard': self.leaderboard,
            'error_message': self.error_message
        }

@dataclass
class PredictionRequest:
    """Request for model prediction"""
    model_uuid: str
    data: List[Dict[str, Any]]
    
@dataclass
class PredictionResult:
    """Result of model prediction"""
    success: bool
    predictions: Optional[List[Any]] = None
    probabilities: Optional[List[List[float]]] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'predictions': self.predictions,
            'probabilities': self.probabilities,
            'error_message': self.error_message
        }