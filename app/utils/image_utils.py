import os
import logging
from typing import Tuple, Optional
from PIL import Image
from werkzeug.datastructures import FileStorage
from config.config import Config

logger = logging.getLogger(__name__)

def allowed_file(filename: str) -> bool:
    """
    Verifica si el archivo tiene una extensión permitida
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        bool: True si la extensión está permitida
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_image_file(file: FileStorage) -> Tuple[bool, str]:
    """
    Valida un archivo de imagen
    
    Args:
        file: Archivo subido
        
    Returns:
        Tuple[bool, str]: (es_válido, mensaje_error)
    """
    if not file:
        return False, "No se proporcionó ningún archivo"
    
    if file.filename == '':
        return False, "No se seleccionó ningún archivo"
    
    if not allowed_file(file.filename):
        return False, f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(Config.ALLOWED_EXTENSIONS)}"
    
    # Verificar el tamaño del archivo
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > Config.MAX_CONTENT_LENGTH:
        return False, f"El archivo es demasiado grande. Tamaño máximo permitido: {Config.MAX_CONTENT_LENGTH / (1024*1024):.1f}MB"
    
    return True, ""

def process_uploaded_image(file: FileStorage) -> Optional[Image.Image]:
    """
    Procesa y convierte un archivo subido a imagen PIL
    
    Args:
        file: Archivo subido
        
    Returns:
        Image.Image o None si hay error
    """
    try:
        # Validar el archivo
        is_valid, error_message = validate_image_file(file)
        if not is_valid:
            logger.error(f"Archivo inválido: {error_message}")
            return None
        
        # Intentar abrir la imagen
        image = Image.open(file.stream)
        
        # Verificar que sea una imagen válida
        image.verify()
        
        # Reabrir la imagen para uso (verify() cierra el archivo)
        file.stream.seek(0)
        image = Image.open(file.stream)
        
        logger.info(f"Imagen procesada exitosamente: {file.filename}, Tamaño: {image.size}, Modo: {image.mode}")
        return image
        
    except Exception as e:
        logger.error(f"Error al procesar imagen: {str(e)}")
        return None

def get_image_info(image: Image.Image) -> dict:
    """
    Obtiene información básica de una imagen
    
    Args:
        image: Imagen PIL
        
    Returns:
        dict: Información de la imagen
    """
    return {
        'format': image.format,
        'mode': image.mode,
        'size': image.size,
        'width': image.width,
        'height': image.height
    }
