# BE/app/routes/predictions_routes.py
from flask import Blueprint, request, jsonify
import logging
from typing import Dict, Any, List

from services.container import get_model_service
from utils.request_validators import validate_uuid, validate_prediction_request

logger = logging.getLogger(__name__)

predictions_bp = Blueprint('predictions', __name__, url_prefix='/api/predictions')

@predictions_bp.route('/<model_uuid>/predict', methods=['POST'])
def predict(model_uuid: str):
    """
    Make predictions using a trained model
    
    Expected JSON payload:
    {
        "data": [
            {
                "feature1": value1,
                "feature2": value2,
                ...
            },
            {
                "feature1": value1,
                "feature2": value2,
                ...
            }
        ]
    }
    
    Returns:
    {
        "success": true,
        "model_uuid": "string",
        "model_name": "string",
        "predictions": [value1, value2, ...],
        "probabilities": [[prob1, prob2], ...] // for classification only
        "target_feature": "string"
    }
    """
    try:
        # Validate UUID format
        if not validate_uuid(model_uuid):
            return jsonify({'error': 'Invalid UUID format'}), 400
        
        # Validate request payload
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload'}), 400
        
        validation_error = validate_prediction_request(data)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        prediction_data = data.get('data', [])
        
        if not prediction_data:
            return jsonify({'error': 'No prediction data provided'}), 400
        
        # Get model service and make predictions
        model_service = get_model_service()
        result = model_service.predict(model_uuid, prediction_data)
        
        if result['success']:
            logger.info(f"Prediction completed for model: {model_uuid}, {len(prediction_data)} samples")
            return jsonify(result), 200
        else:
            logger.error(f"Prediction failed for model {model_uuid}: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in prediction for {model_uuid}: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@predictions_bp.route('/<model_uuid>/predict/batch', methods=['POST'])
def predict_batch(model_uuid: str):
    """
    Make batch predictions with file upload support
    
    Expected form data:
    - file: CSV file with prediction data
    
    Or JSON payload similar to /predict but for larger datasets
    """
    try:
        # Validate UUID format
        if not validate_uuid(model_uuid):
            return jsonify({'error': 'Invalid UUID format'}), 400
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not file.filename.lower().endswith('.csv'):
                return jsonify({'error': 'Only CSV files are supported'}), 400
            
            try:
                import pandas as pd
                import io
                
                # Read CSV file
                csv_content = file.read().decode('utf-8')
                df = pd.read_csv(io.StringIO(csv_content))
                
                # Convert to list of dictionaries
                prediction_data = df.to_dict('records')
                
            except Exception as e:
                return jsonify({'error': f'Error processing CSV file: {str(e)}'}), 400
        
        # Handle JSON payload
        else:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON payload or no file provided'}), 400
            
            prediction_data = data.get('data', [])
        
        if not prediction_data:
            return jsonify({'error': 'No prediction data provided'}), 400
        
        # Limit batch size for performance
        max_batch_size = 10000
        if len(prediction_data) > max_batch_size:
            return jsonify({
                'error': f'Batch size too large. Maximum {max_batch_size} samples allowed'
            }), 400
        
        # Get model service and make predictions
        model_service = get_model_service()
        result = model_service.predict(model_uuid, prediction_data)
        
        if result['success']:
            logger.info(f"Batch prediction completed for model: {model_uuid}, {len(prediction_data)} samples")
            
            # Add batch processing information
            result['batch_info'] = {
                'total_samples': len(prediction_data),
                'processing_time': None  # Could add timing info
            }
            
            return jsonify(result), 200
        else:
            logger.error(f"Batch prediction failed for model {model_uuid}: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        logger.error(f"Unexpected error in batch prediction for {model_uuid}: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@predictions_bp.route('/<model_uuid>/predict/sample', methods=['GET'])
def get_prediction_sample(model_uuid: str):
    """
    Get a sample of the expected input format for predictions
    """
    try:
        # Validate UUID format
        if not validate_uuid(model_uuid):
            return jsonify({'error': 'Invalid UUID format'}), 400
        
        model_service = get_model_service()
        model = model_service.get_model_by_uuid(model_uuid)
        
        if model is None:
            return jsonify({'error': 'Model not found'}), 404
        
        # Get feature columns
        feature_columns = model.get('feature_columns', [])
        
        if not feature_columns:
            return jsonify({
                'error': 'Feature information not available for this model'
            }), 400
        
        # Create sample data structure
        sample_data = {
            'data': [
                {col: f'<{col}_value>' for col in feature_columns if col != model['target_feature']}
            ]
        }
        
        return jsonify({
            'success': True,
            'model_uuid': model_uuid,
            'model_name': model['name'],
            'target_feature': model['target_feature'],
            'required_features': [col for col in feature_columns if col != model['target_feature']],
            'sample_request': sample_data,
            'example_curl': f"""curl -X POST {request.url_root}api/predictions/{model_uuid}/predict \\
  -H "Content-Type: application/json" \\
  -d '{{"data": [{{{', '.join([f'"{col}": "value"' for col in feature_columns if col != model['target_feature']])}}}]}}'"""
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting prediction sample for {model_uuid}: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500