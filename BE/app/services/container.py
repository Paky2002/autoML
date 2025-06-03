# BE/app/services/container.py
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ServiceContainer:
    """Dependency Injection Container for managing service instances"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
        self._initialized = False
    
    def initialize(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the container with default or custom configurations"""
        if self._initialized:
            return
        
        config = config or {}
        
        try:
            # Import services only when needed to avoid circular imports
            from services.ml_service import AutoGluonMLService
            from repositories.model_repository import ModelRepository
            from services.model_service import ModelService
            
            # Initialize ML Service
            ml_service_config = config.get('ml_service', {})
            models_path = ml_service_config.get('models_path', 'models_output')
            
            ml_service = AutoGluonMLService(models_base_path=models_path)
            self.register_singleton('ml_service', ml_service)
            
            # Initialize Repository
            model_repository = ModelRepository()
            self.register_singleton('model_repository', model_repository)
            
            # Initialize Model Service
            model_service = ModelService(
                ml_service=ml_service,
                model_repository=model_repository
            )
            self.register_singleton('model_service', model_service)
            
            self._initialized = True
            logger.info("Service container initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize service container: {str(e)}")
            raise
    
    def register_singleton(self, name: str, instance: Any) -> None:
        """Register a singleton service instance"""
        self._singletons[name] = instance
        logger.debug(f"Registered singleton service: {name}")
    
    def register_factory(self, name: str, factory_func: callable) -> None:
        """Register a factory function for creating service instances"""
        self._services[name] = factory_func
        logger.debug(f"Registered factory service: {name}")
    
    def get(self, name: str) -> Any:
        """Get a service instance by name"""
        # Check singletons first
        if name in self._singletons:
            return self._singletons[name]
        
        # Check factories
        if name in self._services:
            return self._services[name]()
        
        raise ValueError(f"Service '{name}' not found in container")
    
    def get_model_service(self):
        """Get the model service instance"""
        return self.get('model_service')
    
    def get_ml_service(self):
        """Get the ML service instance"""
        return self.get('ml_service')
    
    def get_model_repository(self):
        """Get the model repository instance"""
        return self.get('model_repository')
    
    def clear(self) -> None:
        """Clear all registered services"""
        self._services.clear()
        self._singletons.clear()
        self._initialized = False
        logger.info("Service container cleared")

# Global container instance
_container = ServiceContainer()

def get_container() -> ServiceContainer:
    """Get the global service container instance"""
    return _container

def initialize_services(config: Optional[Dict[str, Any]] = None) -> None:
    """Initialize all services with configuration"""
    _container.initialize(config)

def get_model_service():
    """Convenience function to get model service"""
    return _container.get_model_service()

def get_ml_service():
    """Convenience function to get ML service"""
    return _container.get_ml_service()

def get_model_repository():
    """Convenience function to get model repository"""
    return _container.get_model_repository()