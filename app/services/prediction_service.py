import os
import logging
import requests
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
        self.model_url = os.environ.get('MODEL_URL', 'https://huggingface.co/risehit/tomato_leaf_classifier/resolve/main/models/tomato_leaf_classifier.keras')
        
    def download_model(self) -> bool:
        """
        Descarga el modelo desde Hugging Face si no existe localmente
        
        Returns:
            bool: True si el modelo se descargó correctamente, False en caso contrario
        """
        try:
            model_path = Config.MODEL_PATH
            
            if os.path.exists(model_path):
                logger.info(f"Modelo ya existe en {model_path}")
                return True
            
            logger.info(f"📥 Descargando modelo desde Hugging Face...")
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Descargar modelo
            response = requests.get(self.model_url, stream=True)
            response.raise_for_status()
            
            # Guardar modelo con barra de progreso
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Log progreso cada 10MB
                        if downloaded_size % (10 * 1024 * 1024) == 0:
                            progress = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                            logger.info(f"📥 Descarga en progreso: {progress:.1f}%")
            
            logger.info(f"✅ Modelo descargado exitosamente en {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error descargando modelo: {str(e)}")
            return False
    
    def load_model(self) -> bool:
        """
        Carga el modelo de clasificación, descargándolo si es necesario
        
        Returns:
            bool: True si el modelo se cargó correctamente, False en caso contrario
        """
        try:
            # Descargar modelo si no existe
            if not self.download_model():
                logger.error("No se pudo descargar el modelo")
                return False
            
            model_path = Config.MODEL_PATH
            
            if not os.path.exists(model_path):
                logger.error(f"Modelo no encontrado en {model_path} después de la descarga")
                return False
                
            self.model = load_model(model_path)
            self.is_model_loaded = True
            logger.info(f"✅ Modelo cargado exitosamente desde {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al cargar el modelo: {str(e)}")
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
        logger.info(f"Iniciando predicción. Modelo cargado: {self.is_model_loaded}")
        
        try:
            if self.is_model_loaded and self.model is not None:
                logger.info("Usando modelo real para predicción")
                processed_image = self.preprocess_image(image)
                predictions = self.model.predict(processed_image, verbose=0)
                
                # Obtener la clase con mayor probabilidad
                predicted_class_index = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_class_index])
                predicted_class = self.class_names[predicted_class_index]
                
                result = {
                    'prediction': predicted_class,
                    'confidence': round(confidence * 100, 2),
                    'all_predictions': {
                        class_name: round(float(prob) * 100, 2) 
                        for class_name, prob in zip(self.class_names, predictions[0])
                    },
                    'model_used': True
                }
                logger.info(f"Predicción con modelo real completada: {predicted_class}")
                return result
            else:
                # Error: modelo no disponible
                logger.error("Modelo de IA no disponible - servicio no puede procesar la imagen")
                raise Exception("Modelo de clasificación no disponible")
                
        except Exception as e:
            logger.error(f"Error durante la predicción: {str(e)}")
            # Re-raise para que se maneje como error en routes
            raise
            return self._simulate_prediction()
# Instancia global del servicio
prediction_service = PredictionService()
