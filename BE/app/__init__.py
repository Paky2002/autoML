# BE/app/__init__.py
from flask import Flask
from flask_cors import CORS
import logging
import os
from pathlib import Path

from config.config import Config
from extensions import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Application factory pattern"""
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for frontend communication
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize extensions
    db.init_app(app)
    
    # Create necessary directories
    models_dir = Path(app.config.get('MODELS_PATH', 'models_output'))
    models_dir.mkdir(exist_ok=True)
    
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Import models to ensure tables are created
    from models import TrainedModel
    
    # Register routes
    from routes import register_routes
    register_routes(app)
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {str(e)}")
        return {'error': 'An unexpected error occurred'}, 500
    
    logger.info("Flask application created successfully")
    return app