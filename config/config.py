import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_IMAGE_SIZE', 5242880))  # 5MB por defecto
    
    # Configuración del modelo
    MODEL_PATH = os.environ.get('MODEL_PATH', 'models/tomato_classifier.keras')
    ALLOWED_EXTENSIONS = set(os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif').split(','))
    
    # Configuración del servidor
    HOST = os.environ.get('HOST', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configuración de CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000,https://mcd-scanveg-ai.pages.dev').split(',')

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Configuración
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 10000))
    
    # Configuración de CORS para producción
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',') if os.environ.get('CORS_ORIGINS') != '*' else ['*']

# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
