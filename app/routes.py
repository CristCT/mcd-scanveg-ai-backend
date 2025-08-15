import logging
from flask import Blueprint, request
from app.services.prediction_service import prediction_service
from app.utils.image_utils import process_uploaded_image
from app.utils.response_utils import success_response, error_response

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    """
    Endpoint raíz - información básica del servicio
    """
    return success_response(
        data={
            "service": "MCD ScanVeg AI Backend",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "health": "/api/ping",
                "scan": "/api/scan",
                "model_info": "/api/model/info"
            }
        },
        message="Bienvenido al backend de MCD ScanVeg AI"
    )

@main.route('/ping', methods=['GET'])
def ping():
    """
    Endpoint de health check
    """
    return success_response(
        data={"status": "healthy", "service": "MCD ScanVeg AI Backend"},
        message="Servicio funcionando correctamente"
    )

@main.route('/scan', methods=['POST'])
def scan_vegetable():
    """
    Endpoint principal para clasificar vegetales
    Recibe una imagen y retorna la predicción del modelo
    """
    try:
        # Verificar que se envió un archivo
        if 'image' not in request.files:
            logger.warning("Request sin campo 'image'")
            error_resp = error_response(
                message="No se encontró el campo 'image' en la petición",
                error_code="MISSING_IMAGE_FIELD"
            )
            logger.info(f"Enviando error al frontend: {error_resp[0].get_json()}")
            return error_resp
        
        file = request.files['image']
        
        # Procesar la imagen
        image = process_uploaded_image(file)
        if image is None:
            logger.warning(f"Archivo de imagen inválido: {file.filename}")
            error_resp = error_response(
                message="Error al procesar la imagen. Verifique que sea un archivo de imagen válido.",
                error_code="INVALID_IMAGE_FILE"
            )
            return error_resp
        
        logger.info(f"Procesando imagen para clasificación: {file.filename}")
        
        # Realizar la predicción
        prediction_result = prediction_service.predict(image)
        logger.info(f"Resultado de predicción: {prediction_result}")
        logger.info(f"Tipo de resultado: {type(prediction_result)}")
        
        # Verificar que el resultado no sea None
        if prediction_result is None:
            logger.error("El servicio de predicción retornó None")
            return error_response(
                message="Error en el servicio de predicción",
                status_code=500,
                error_code="PREDICTION_SERVICE_ERROR"
            )
        
        # Verificar que tenga las claves necesarias
        if 'prediction' not in prediction_result:
            logger.error(f"Resultado de predicción no tiene clave 'prediction': {prediction_result}")
            return error_response(
                message="Respuesta inválida del servicio de predicción",
                status_code=500,
                error_code="INVALID_PREDICTION_RESPONSE"
            )
        
        # Preparar la respuesta
        response_data = {
            'prediction': prediction_result['prediction'],
            'confidence': prediction_result['confidence'],
            'model_info': {
                'model_used': prediction_result.get('model_used', False),
                'available_classes': prediction_service.class_names
            }
        }
        
        # Incluir predicciones detalladas si están disponibles
        if 'all_predictions' in prediction_result:
            response_data['detailed_predictions'] = prediction_result['all_predictions']
        
        # Incluir nota si es predicción simulada
        if 'note' in prediction_result:
            response_data['note'] = prediction_result['note']
        
        logger.info(f"Predicción exitosa: {prediction_result['prediction']} ({prediction_result['confidence']}%)")
        
        success_resp = success_response(
            data=response_data,
            message="Clasificación completada exitosamente"
        )
        logger.info(f"Enviando respuesta exitosa al frontend: {success_resp[0].get_json()}")
        return success_resp
        
    except Exception as e:
        logger.error(f"Error durante la clasificación: {str(e)}")
        error_resp = error_response(
            message="Error general del servicio",
            status_code=500,
            error_code="SERVICE_ERROR"
        )
        logger.info(f"Enviando error 500 al frontend: {error_resp[0].get_json()}")
        return error_resp

@main.route('/model/info', methods=['GET'])
def model_info():
    """
    Endpoint para obtener información del modelo
    """
    try:
        model_info = {
            'model_loaded': prediction_service.is_model_loaded,
            'model_path': prediction_service.model.name if prediction_service.is_model_loaded else None,
            'available_classes': prediction_service.class_names,
            'total_classes': len(prediction_service.class_names)
        }
        
        return success_response(
            data=model_info,
            message="Información del modelo obtenida exitosamente"
        )
        
    except Exception as e:
        logger.error(f"Error al obtener información del modelo: {str(e)}")
        return error_response(
            message="Error al obtener información del modelo",
            status_code=500,
            error_code="MODEL_INFO_ERROR"
        )
