# BE/app/utils/request_validators.py
import re
import uuid
from typing import Dict, Any, Optional, List

def validate_uuid(uuid_string: str) -> bool:
    """Validate UUID format"""
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False

def validate_training_request(data: Dict[str, Any]) -> Optional[str]:
    """
    Validate training request payload
    
    Returns:
        None if valid, error message string if invalid
    """
    # Check required top-level keys
    if 'dataset' not in data:
        return "Missing 'dataset' in request"
    
    if 'config' not in data:
        return "Missing 'config' in request"
    
    # Validate dataset
    dataset = data['dataset']
    dataset_error = validate_dataset(dataset)
    if dataset_error:
        return f"Dataset validation error: {dataset_error}"
    
    # Validate config
    config = data['config']
    config_error = validate_training_config(config)
    if config_error:
        return f"Config validation error: {config_error}"
    
    # Cross-validation: target feature must be in dataset headers
    target_feature = config.get('targetFeature')
    headers = dataset.get('headers', [])
    
    if target_feature not in headers:
        return f"Target feature '{target_feature}' not found in dataset headers"
    
    return None

def validate_dataset(dataset: Dict[str, Any]) -> Optional[str]:
    """Validate dataset structure"""
    required_fields = ['filename', 'headers', 'rows']
    
    for field in required_fields:
        if field not in dataset:
            return f"Missing required field: {field}"
    
    # Validate filename
    filename = dataset['filename']
    if not isinstance(filename, str) or not filename.strip():
        return "Filename must be a non-empty string"
    
    # Validate headers
    headers = dataset['headers']
    if not isinstance(headers, list) or len(headers) == 0:
        return "Headers must be a non-empty list"
    
    if not all(isinstance(h, str) and h.strip() for h in headers):
        return "All headers must be non-empty strings"
    
    # Check for duplicate headers
    if len(headers) != len(set(headers)):
        return "Headers must be unique"
    
    # Validate rows
    rows = dataset['rows']
    if not isinstance(rows, list):
        return "Rows must be a list"
    
    if len(rows) == 0:
        return "Dataset must contain at least one row"
    
    # Check row consistency
    expected_columns = len(headers)
    for i, row in enumerate(rows[:10]):  # Check first 10 rows for performance
        if not isinstance(row, list):
            return f"Row {i} must be a list"
        
        if len(row) != expected_columns:
            return f"Row {i} has {len(row)} columns, expected {expected_columns}"
    
    return None

def validate_training_config(config: Dict[str, Any]) -> Optional[str]:
    """Validate training configuration"""
    required_fields = ['modelName', 'targetFeature', 'problemType']
    
    for field in required_fields:
        if field not in config:
            return f"Missing required field: {field}"
    
    # Validate model name
    model_name = config['modelName']
    if not isinstance(model_name, str) or not model_name.strip():
        return "Model name must be a non-empty string"
    
    if len(model_name) > 255:
        return "Model name must be less than 255 characters"
    
    # Validate target feature
    target_feature = config['targetFeature']
    if not isinstance(target_feature, str) or not target_feature.strip():
        return "Target feature must be a non-empty string"
    
    # Validate problem type
    problem_type = config['problemType']
    valid_types = ['regression', 'binary', 'multiclass', 'auto']
    if problem_type not in valid_types:
        return f"Problem type must be one of: {valid_types}"
    
    # Validate optional fields
    if 'timeLimit' in config:
        time_limit = config['timeLimit']
        if not isinstance(time_limit, int) or time_limit <= 0:
            return "Time limit must be a positive integer"
        
        if time_limit > 7200:  # 2 hours max
            return "Time limit cannot exceed 7200 seconds (2 hours)"
    
    if 'verbosity' in config:
        verbosity = config['verbosity']
        if not isinstance(verbosity, int) or verbosity not in [0, 1, 2, 3]:
            return "Verbosity must be an integer between 0 and 3"
    
    if 'presets' in config:
        presets = config['presets']
        valid_presets = ['best_quality', 'good_quality_faster', 'optimize_for_deployment']
        if presets not in valid_presets:
            return f"Presets must be one of: {valid_presets}"
    
    if 'evalMetric' in config:
        eval_metric = config['evalMetric']
        if eval_metric is not None and (not isinstance(eval_metric, str) or not eval_metric.strip()):
            return "Evaluation metric must be a non-empty string or null"
    
    return None

def validate_prediction_request(data: Dict[str, Any]) -> Optional[str]:
    """Validate prediction request payload"""
    if 'data' not in data:
        return "Missing 'data' in request"
    
    prediction_data = data['data']
    
    if not isinstance(prediction_data, list):
        return "Prediction data must be a list"
    
    if len(prediction_data) == 0:
        return "Prediction data cannot be empty"
    
    if len(prediction_data) > 1000:  # Limit for single request
        return "Too many samples in single request. Use batch endpoint for > 1000 samples"
    
    # Validate each sample
    for i, sample in enumerate(prediction_data[:5]):  # Check first 5 samples
        if not isinstance(sample, dict):
            return f"Sample {i} must be a dictionary"
        
        if len(sample) == 0:
            return f"Sample {i} cannot be empty"
        
        # Check for consistent keys across samples
        if i == 0:
            expected_keys = set(sample.keys())
        else:
            if set(sample.keys()) != expected_keys:
                return f"Sample {i} has different keys than sample 0. All samples must have the same features"
    
    return None

def validate_model_name(name: str) -> bool:
    """Validate model name format"""
    if not isinstance(name, str):
        return False
    
    # Must be non-empty, max 255 chars, alphanumeric + spaces/dashes/underscores
    pattern = r'^[a-zA-Z0-9\s\-_]{1,255}$'
    return bool(re.match(pattern, name.strip()))

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    safe_chars = re.sub(r'[^\w\-_\.]', '_', filename)
    return safe_chars[:255]  # Limit length