# BE/app/routes/__init__.py
from flask import Flask
import logging

from routes.training_routes import training_bp
from routes.models_routes import models_bp
from routes.predictions_routes import predictions_bp
from services.container import initialize_services

logger = logging.getLogger(__name__)

def register_routes(app: Flask):
    """Register all route blueprints with the Flask app"""
    
    # Initialize services before registering routes
    try:
        # Get configuration from app config if available
        models_config = {
            'ml_service': {
                'models_path': app.config.get('MODELS_PATH', 'models_output')
            }
        }
        initialize_services(models_config)
        logger.info("Services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise
    
    # Register all blueprints
    app.register_blueprint(training_bp)
    app.register_blueprint(models_bp)
    app.register_blueprint(predictions_bp)
    
    logger.info("All route blueprints registered successfully")
    
    # Add health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'AutoML API',
            'version': '1.0.0'
        }, 200
    
    # Add API documentation endpoint
    @app.route('/api/docs', methods=['GET'])
    def api_docs():
        """API documentation endpoint"""
        return {
            'api_version': '1.0.0',
            'endpoints': {
                'training': {
                    'POST /api/training/train': 'Train a new model',
                    'GET /api/training/status/<uuid>': 'Get training status'
                },
                'models': {
                    'GET /api/models': 'List all models',
                    'GET /api/models/<uuid>': 'Get model details',
                    'DELETE /api/models/<uuid>': 'Delete a model',
                    'GET /api/models/<uuid>/info': 'Get model ML info'
                },
                'predictions': {
                    'POST /api/predictions/<uuid>/predict': 'Make predictions',
                    'POST /api/predictions/<uuid>/predict/batch': 'Batch predictions',
                    'GET /api/predictions/<uuid>/predict/sample': 'Get prediction sample'
                },
                'utility': {
                    'GET /api/health': 'Health check',
                    'GET /api/docs': 'API documentation'
                }
            }
        }, 200