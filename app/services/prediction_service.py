import os
import logging
from typing import Optional, Dict, Any
import numpy as np
from PIL import Image
from tensorflow import keras
from tensorflow.keras.models import load_model
from config.config import Config

logger = logging.getLogger(__name__)

class PredictionService:
    """Servicio para realizar predicciones con el modelo de IA"""
    
    def __init__(self):
        self.model: Optional[keras.Model] = None
        self.class_names = [
            'Zanahoria', 'Brócoli', 'Tomate', 'Lechuga', 'Pimiento',
            'Cebolla', 'Papa', 'Apio', 'Pepino', 'Calabacín'
        ]
        self.is_model_loaded = False
        
    def load_model(self) -> bool:
        """
        Carga el modelo de clasificación desde el archivo .keras
        
        Returns:
            bool: True si el modelo se cargó correctamente, False en caso contrario
        """
        try:
            model_path = Config.MODEL_PATH
            
            if not os.path.exists(model_path):
                logger.warning(f"Modelo no encontrado en {model_path}. Usando predicción simulada.")
                return False
                
            self.model = load_model(model_path)
            self.is_model_loaded = True
            logger.info(f"Modelo cargado exitosamente desde {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {str(e)}")
            return False
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocesa la imagen para el modelo
        
        Args:
            image: Imagen PIL
            
        Returns:
            np.ndarray: Imagen preprocesada como array numpy
        """
        try:
            # Redimensionar a 224x224
            image = image.resize((224, 224))
            
            # Convertir a RGB si es necesario
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convertir a array numpy y normalizar
            image_array = np.array(image) / 255.0
            
            # Añadir dimensión del batch
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error al preprocesar imagen: {str(e)}")
            raise
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """
        Realiza una predicción sobre la imagen
        
        Args:
            image: Imagen PIL a clasificar
            
        Returns:
            Dict con la predicción, confianza y otros datos
        """
        try:
            if self.is_model_loaded and self.model is not None:
                processed_image = self.preprocess_image(image)
                predictions = self.model.predict(processed_image, verbose=0)
                
                # Obtener la clase con mayor probabilidad
                predicted_class_index = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_class_index])
                predicted_class = self.class_names[predicted_class_index]
                
                return {
                    'prediction': predicted_class,
                    'confidence': round(confidence * 100, 2),
                    'all_predictions': {
                        class_name: round(float(prob) * 100, 2) 
                        for class_name, prob in zip(self.class_names, predictions[0])
                    },
                    'model_used': True
                }
                
        except Exception as e:
            logger.error(f"Error durante la predicción: {str(e)}")

# Instancia global del servicio
prediction_service = PredictionService()
