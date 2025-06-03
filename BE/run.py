# BE/run.py
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
current_dir = Path(__file__).parent
app_dir = current_dir / 'app'
sys.path.insert(0, str(app_dir))

# Import the create_app function
from app import create_app
from config.config import config

def main():
    """Main application entry point"""
    
    # Get environment configuration
    env = os.getenv('FLASK_ENV', 'development')
    config_class = config.get(env, config['default'])
    
    # Create Flask application
    app = create_app(config_class)
    
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true' and env == 'development'
    
    print(f"Starting AutoML API server...")
    print(f"Environment: {env}")
    print(f"Debug mode: {debug}")
    print(f"Server: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/api/docs")
    print(f"Health Check: http://{host}:{port}/api/health")
    
    # Run the Flask server
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug,
        threaded=True
    )

if __name__ == "__main__":
    main()