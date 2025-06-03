# BE/app/models/__init__.py
from extensions import db
import uuid
from datetime import datetime

class TrainedModel(db.Model):
    __tablename__ = 'trained_models'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    model_path = db.Column(db.String(500), nullable=False)
    
    # Training configuration
    target_feature = db.Column(db.String(255), nullable=False)
    problem_type = db.Column(db.String(50), nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    eval_metric = db.Column(db.String(100))
    presets = db.Column(db.String(100))
    verbosity = db.Column(db.Integer)
    
    # Model status and results
    status = db.Column(db.String(50), default='training')  # training, completed, failed, deleted
    best_score = db.Column(db.Float)
    best_model_name = db.Column(db.String(255))
    error_message = db.Column(db.Text)
    
    # Metadata
    dataset_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'model_path': self.model_path,
            'target_feature': self.target_feature,
            'problem_type': self.problem_type,
            'time_limit': self.time_limit,
            'eval_metric': self.eval_metric,
            'presets': self.presets,
            'verbosity': self.verbosity,
            'status': self.status,
            'best_score': self.best_score,
            'best_model_name': self.best_model_name,
            'error_message': self.error_message,
            'dataset_filename': self.dataset_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<TrainedModel {self.name} ({self.uuid}) - {self.status}>'