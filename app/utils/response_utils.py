from typing import Any, Dict, Optional
from flask import jsonify, Response

def success_response(data: Any = None, message: str = "Operación exitosa", status_code: int = 200) -> Response:
    """
    Genera una respuesta de éxito estandarizada
    
    Args:
        data: Datos a retornar
        message: Mensaje de éxito
        status_code: Código de estado HTTP
        
    Returns:
        Response: Respuesta JSON estandarizada
    """
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message: str, status_code: int = 400, error_code: Optional[str] = None) -> Response:
    """
    Genera una respuesta de error estandarizada
    
    Args:
        message: Mensaje de error
        status_code: Código de estado HTTP
        error_code: Código de error específico
        
    Returns:
        Response: Respuesta JSON de error estandarizada
    """
    response = {
        'success': False,
        'message': message,
        'error_code': error_code,
        'data': None
    }
    return jsonify(response), status_code

def validation_error_response(errors: Dict[str, str]) -> Response:
    """
    Genera una respuesta de error de validación
    
    Args:
        errors: Diccionario con errores de validación
        
    Returns:
        Response: Respuesta JSON de error de validación
    """
    response = {
        'success': False,
        'message': 'Errores de validación',
        'errors': errors,
        'data': None
    }
    return jsonify(response), 422
