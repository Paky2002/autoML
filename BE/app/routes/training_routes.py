# BE/app/routes/training_routes.py
from flask import Blueprint, request, jsonify
import logging
from typing import Dict, Any

from services.base import TrainingConfig, DatasetInfo, ProblemType
from services.container import get_model_service
from utils.request_validators import validate_training_request

logger = logging.getLogger(__name__)

training_bp = Blueprint('training', __name__, url_prefix='/api/training')

@training_bp.route('/train', methods=['POST'])
def train_model():
    """
    Train a new machine learning model
    
    Expected JSON payload:
    {
        "dataset": {
            "filename": "string",
            "headers": ["col1", "col2", ...],
            "rows": [[val1, val2, ...], ...],
            "total_rows": int,
            "file_size": int
        },
        "config": {
            "modelName": "string",
            "targetFeature": "string",
            "problemType": "regression|binary|multiclass|auto",
            "timeLimit": int,
            "evalMetric": "string (optional)",
            "presets": "best_quality|good_quality_faster|optimize_for_deployment",
            "verbosity": int
        }
    }
    """
    try:
        # Validate request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload'}), 400
        
        validation_error = validate_training_request(data)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        # Extract and parse dataset
        dataset_data = data.get('dataset')
        dataset = DatasetInfo(
            filename=dataset_data['filename'],
            headers=dataset_data['headers'],
            rows=dataset_data['rows'],
            total_rows=dataset_data.get('total_rows', len(dataset_data['rows'])),
            file_size=dataset_data.get('file_size', 0)
        )
        
        # Extract and parse training configuration
        config_data = data.get('config')
        config = TrainingConfig(
            model_name=config_data['modelName'],
            target_feature=config_data['targetFeature'],
            problem_type=ProblemType(config_data.get('problemType', 'auto')),
            time_limit=config_data.get('timeLimit', 600),
            eval_metric=config_data.get('evalMetric'),
            presets=config_data.get('presets', 'best_quality'),
            verbosity=config_data.get('verbosity', 2)
        )
        
        # Get model service and start training
        model_service = get_model_service()
        result = model_service.train_model(dataset, config)
        
        if result['success']:
            logger.info(f"Training started successfully for model: {result['model_uuid']}")
            return jsonify({
                'success': True,
                'message': 'Model training completed successfully',
                'data': result
            }), 200
        else:
            logger.error(f"Training failed: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except ValueError as e:
        logger.warning(f"Validation error in training: {str(e)}")
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error in training: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@training_bp.route('/status/<model_uuid>', methods=['GET'])
def get_training_status(model_uuid: str):
    """
    Get the training status of a specific model
    """
    try:
        model_service = get_model_service()
        status = model_service.get_model_status(model_uuid)
        
        if status is None:
            return jsonify({'error': 'Model not found'}), 404
        
        return jsonify({
            'success': True,
            'model_uuid': model_uuid,
            'status': status
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting training status for {model_uuid}: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500