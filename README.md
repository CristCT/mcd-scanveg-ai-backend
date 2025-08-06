# MCD ScanVeg AI - Backend

Backend de clasificación de vegetales con inteligencia artificial desarrollado con Flask.

## 🚀 Características

- **Clasificación de vegetales**: Endpoints para clasificar imágenes de vegetales usando IA
- **API RESTful**: Endpoints bien estructurados con respuestas JSON estandarizadas
- **Soporte de IA**: Compatible con modelos TensorFlow/Keras (.keras)
- **Validación de imágenes**: Validación robusta de archivos de imagen
- **CORS habilitado**: Configurado para trabajar con aplicaciones frontend
- **Configuración por entorno**: Soporte para desarrollo y producción
- **Logging**: Sistema de logging configurado
- **Manejo de errores**: Respuestas de error estandarizadas

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py           # Factory de la aplicación Flask
│   ├── routes.py             # Rutas y endpoints de la API
│   ├── services/ 
│   │   ├── __init__.py
│   │   └── prediction_service.py  # Servicio de predicción con IA
│   └── utils/
│       ├── __init__.py
│       ├── image_utils.py    # Utilidades para procesamiento de imágenes
│       └── response_utils.py # Utilidades para respuestas HTTP
├── config/
│   ├── __init__.py
│   └── config.py             # Configuraciones de la aplicación
├── models/                   # Directorio para modelos .keras
├── .env                      # Variables de entorno (no incluir en git)
├── .env.example              # Ejemplo de variables de entorno
├── .gitignore
├── requirements.txt          # Dependencias de Python
├── run.py                    # Punto de entrada de la aplicación
└── README.md
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar e instalar dependencias

```bash
# Navegar al directorio del backend
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
notepad .env  # En Windows
```

Variables de entorno disponibles:
- `FLASK_ENV`: Entorno de ejecución (development/production)
- `FLASK_DEBUG`: Habilitar modo debug (True/False)
- `MODEL_PATH`: Ruta al modelo .keras
- `MAX_IMAGE_SIZE`: Tamaño máximo de imagen en bytes
- `ALLOWED_EXTENSIONS`: Extensiones de archivo permitidas
- `HOST`: Dirección IP del servidor
- `PORT`: Puerto del servidor

### 3. (Opcional) Agregar modelo de IA

Si tienes un modelo entrenado:

1. Coloca tu archivo `.keras` en el directorio `models/`
2. Actualiza `MODEL_PATH` en el archivo `.env`

Si no tienes un modelo, la aplicación funcionará con predicciones simuladas.

## 🚀 Ejecución

### Modo desarrollo

```bash
python run.py
```

### Modo producción

```bash
# Configurar variables de entorno
set FLASK_ENV=production

# Ejecutar
python run.py
```

El servidor estará disponible en: `http://127.0.0.1:5000`

## 📡 API Endpoints

### 1. Health Check

```http
GET /api/ping
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Servicio funcionando correctamente",
  "data": {
    "status": "healthy",
    "service": "MCD ScanVeg AI Backend"
  }
}
```

### 2. Clasificar Vegetal

```http
POST /api/scan
Content-Type: multipart/form-data
```

**Parámetros:**
- `image`: Archivo de imagen (JPG, JPEG, PNG, GIF)

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Clasificación completada exitosamente",
  "data": {
    "prediction": "Tomate",
    "confidence": 87.5,
    "model_info": {
      "model_used": true,
      "available_classes": ["Tomate", ...]
    },
    "detailed_predictions": {
      "Tomate": 87.5,
      ...
    }
  }
}
```

**Respuesta de error:**
```json
{
  "success": false,
  "message": "Error al procesar la imagen",
  "error_code": "INVALID_IMAGE_FILE",
  "data": null
}
```

## 🧪 Pruebas

### Probar con curl

```bash
# Health check
curl http://127.0.0.1:5000/api/ping

# Clasificar imagen
curl -X POST -F "image=@ruta/a/imagen.jpg" http://127.0.0.1:5000/api/scan

# Información del modelo
curl http://127.0.0.1:5000/api/model/info
```

### Probar con frontend

El backend está configurado con CORS para aceptar peticiones desde:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## 🔧 Desarrollo

### Estructura del código

- **`app/__init__.py`**: Factory pattern para crear la aplicación Flask
- **`app/routes.py`**: Definición de endpoints y rutas
- **`app/services/prediction_service.py`**: Lógica de predicción con IA
- **`app/utils/`**: Utilidades para procesamiento de imágenes y respuestas
- **`config/config.py`**: Configuraciones por entorno

### Agregar nuevos endpoints

1. Edita `app/routes.py`
2. Agrega la nueva ruta usando el blueprint `main`
3. Usa las utilidades de respuesta para mantener consistencia

### Cambiar el modelo

1. Coloca el nuevo modelo en `models/`
2. Actualiza `MODEL_PATH` en `.env`
3. Ajusta `class_names` en `prediction_service.py` si es necesario

## 🐛 Solución de problemas

### Error: "Modelo no encontrado"
- Verifica que el archivo `.keras` existe en la ruta especificada

### Error: "Import tensorflow could not be resolved"
- Instala TensorFlow: `pip install tensorflow`
- Verifica que estés en el entorno virtual correcto

### Error: "CORS policy"
- Verifica que el frontend esté en un origen permitido
- Actualiza `CORS_ORIGINS` en `config.py` si es necesario

## 👥 Contribución

1. Fork del proyecto
2. Crear rama para nueva funcionalidad
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.
