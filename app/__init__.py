import os
import logging
from flask import Flask
from flask_cors import CORS
from config.config import config
from app.services.prediction_service import prediction_service

def create_app(config_name: str = None) -> Flask:
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        Flask: Instancia de la aplicación
    """
    # Determinar el entorno
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Crear la aplicación
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configurar CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Configurar logging
    setup_logging(app)
    
    # Inicializar servicios
    with app.app_context():
        initialize_services()
    
    # Registrar blueprints
    from .routes import main
    app.register_blueprint(main, url_prefix='/api')
    
    return app

def setup_logging(app: Flask) -> None:
    """
    Configura el sistema de logging
    
    Args:
        app: Instancia de Flask
    """
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )

def initialize_services() -> None:
    """
    Inicializa los servicios de la aplicación
    """
    try:
        # Cargar el modelo de predicción
        prediction_service.load_model()
        logging.info("Servicios inicializados correctamente")
    except Exception as e:
        logging.error(f"Error al inicializar servicios: {str(e)}")
