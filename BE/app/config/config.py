# BE/app/config/config.py
import os
from pathlib import Path

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///automl.db')
    
    # AutoML specific configuration
    # Calculate path relative to BE directory (where run.py is)
    MODELS_PATH = os.getenv("MODELS_PATH", 
                           os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models_output"))
    MAX_TRAINING_TIME = int(os.getenv("MAX_TRAINING_TIME", "7200"))  # 2 hours max
    MAX_PREDICTION_BATCH_SIZE = int(os.getenv("MAX_PREDICTION_BATCH_SIZE", "10000"))
    
    # Logging configuration
    LOG_TO_STDOUT = os.getenv("LOG_TO_STDOUT", "true").lower() == "true"
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Security settings
    TEMPLATES_AUTO_RELOAD = True
    JSON_SORT_KEYS = False
    
    # File upload limits
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    @staticmethod
    def init_app(app):
        """Initialize app-specific configuration"""
        # Ensure required directories exist
        models_path = Path(app.config['MODELS_PATH'])
        models_path.mkdir(exist_ok=True)
        
        logs_path = Path(app.config['LOG_FILE']).parent
        logs_path.mkdir(exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///automl_dev.db')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///automl_prod.db')
    
    # Production-specific settings
    MAX_TRAINING_TIME = int(os.getenv("MAX_TRAINING_TIME", "3600"))  # 1 hour max in prod
    LOG_LEVEL = "WARNING"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}