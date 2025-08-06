import os
import sys
from app import create_app
from config.config import Config

def main():
    """
    Función principal para ejecutar la aplicación
    """
    # Obtener el entorno de configuración
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Crear la aplicación
    app = create_app(config_name)
    
    print("🍅 MCD ScanVeg AI Backend")
    print("=" * 50)
    print(f"🌟 Entorno: {config_name}")
    print(f"🌐 Host: {Config.HOST}")
    print(f"🚀 Puerto: {Config.PORT}")
    print(f"🔧 Debug: {app.config.get('DEBUG', False)}")
    print("=" * 50)
    print("📡 Endpoints disponibles:")
    print("   GET  /api/ping      - Health check")
    print("   POST /api/scan      - Clasificar vegetal")
    print("   GET  /api/model/info - Información del modelo")
    print("=" * 50)
    
    try:
        # Ejecutar la aplicación
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=app.config.get('DEBUG', False)
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
