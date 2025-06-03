# BE/app/routes/models_routes.py
from flask import Blueprint, request, jsonify
import logging
from typing import Dict, Any

from services.container import get_model_service
from utils.request_validators import validate_uuid

logger = logging.getLogger(__name__)

models_bp = Blueprint('models', __name__, url_prefix='/api/models')

@models_bp.route('', methods=['GET'])
def get_all_models():
    """
    Get all trained models
    
    Returns:
    {
        "success": true,
        "models": [
            {
                "id": int,
                "uuid": "string",
                "name": "string",
                "model_path": "string",
                "target_feature": "string",
                "problem_type": "string",
                "status": "string",
                "created_at": "string",
                ...
            }
        ]
    }
    """
    try:
        model_service = get_model_service()
        models = model_service.get_all_models()
        
        return jsonify({
            'success': True,
            'models': models,
            'count': len(models)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving models: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@models_bp.route('/<model_uuid>', methods=['GET'])
def get_model_by_uuid(model_uuid: str):
    """
    Get a specific model by UUID
    
    Returns detailed information about the model including
    feature importance, leaderboard, etc.
    """
    try:
        # Validate UUID format
        if not validate_uuid(model_uuid):
            return jsonify({'error': 'Invalid UUID format'}), 400
        
        model_service = get_model_service()
        model = model_service.get_model_by_uuid(model_uuid)
        
        if model is None:
            return jsonify({'error': 'Model not found'}), 404
        
        return jsonify({
            'success': True,
            'model': model
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving model {model_uuid}: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@models_bp.route('/<model_uuid>', methods=['DELETE'])
def delete_model(model_uuid: str):
    """
    Delete a specific model by UUID
    
    This will remove the model from database and delete all associated files
    """
    try:
        # Validate UUID format
        if not validate_uuid(model_uuid):
            return jsonify({'error': 'Invalid UUID format'}), 400
        
        model_service = get_model_service()
        success = model_service.delete_model(model_uuid)
        
        if not success:
            return jsonify({'error': 'Model not found'}), 404
        
        logger.info(f"Model {model_uuid} deleted successfully")
        return jsonify({
            'success': True,
            'message': 'Model deleted successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting model {model_uuid}: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@models_bp.route('/<model_uuid>/info', methods=['GET'])
def get_model_info(model_uuid: str):
    """
    Get detailed ML information about a model
    Including feature importance, leaderboard, etc.
    """
    try:
        # Validate UUID format
        if not validate_uuid(model_uuid):
            return jsonify({'error': 'Invalid UUID format'}), 400
        
        model_service = get_model_service()
        model = model_service.get_model_by_uuid(model_uuid)
        
        if model is None:
            return jsonify({'error': 'Model not found'}), 404
        
        # Extract only ML-specific information
        ml_info = {
            'model_uuid': model['uuid'],
            'name': model['name'],
            'status': model['status'],
            'target_feature': model['target_feature'],
            'problem_type': model['problem_type'],
            'feature_columns': model.get('feature_columns', []),
            'feature_importance': model.get('feature_importance'),
            'detailed_leaderboard': model.get('detailed_leaderboard'),
            'best_score': model.get('best_score'),
            'best_model_name': model.get('best_model_name')
        }
        
        return jsonify({
            'success': True,
            'model_info': ml_info
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting model info for {model_uuid}: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500