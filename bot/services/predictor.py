# bot/services/predictor.py
import sys
import os
import logging
from typing import Dict, Any, Optional
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

logger = logging.getLogger(__name__)

class PredictorService:
    """Сервис для работы с ML моделью виральности"""
    
    def __init__(self, model_path: str = None, tokenizer_path: str = None):
        self.model = None
        self.tokenizer = None
        self.is_loaded = False
        
        self.model_path = model_path or "models/complete_model.keras"
        self.tokenizer_path = tokenizer_path or "tokenizers/tokenizer.pkl"
        
        self._load_model()
    
    def _load_model(self):
        """Загрузка модели и токенизатора"""
        try:
            from predictor.viral_predictor import load_model_and_tokenizer
            
            if not os.path.exists(self.model_path):
                logger.error(f"❌ Файл модели не найден: {self.model_path}")
                return
            
            if not os.path.exists(self.tokenizer_path):
                logger.error(f"❌ Файл токенизатора не найден: {self.tokenizer_path}")
                return
            
            load_model_and_tokenizer(self.model_path, self.tokenizer_path)
            self.is_loaded = True
            logger.info(f"✅ Модель загружена: {self.model_path}")
            
        except ImportError as e:
            logger.error(f"❌ Не могу импортировать viral_predictor: {e}")
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки модели: {e}")
    
    async def predict(self, text: str, threshold: float = 0.5) -> Dict[str, Any]:
        """
        Предсказание виральности текста
        
        Args:
            text: Текст для анализа
            threshold: Порог виральности (0-1)
            
        Returns:
            Словарь с результатами предсказания
        """
        if not self.is_loaded:
            return {
                "error": "Модель не загружена",
                "score": 0.5,
                "is_viral": False,
                "confidence": 0.0,
                "text_length": len(text)
            }
        
        if not text or len(text.strip()) < 10:
            return {
                "error": "Текст слишком короткий",
                "score": 0.5,
                "is_viral": False,
                "confidence": 0.0,
                "text_length": len(text)
            }
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._sync_predict,
                text,
                threshold
            )
            
            result["text_length"] = len(text)
            result["text_sample"] = text[:150] + "..." if len(text) > 150 else text
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка предсказания: {e}")
            return {
                "error": str(e),
                "score": 0.5,
                "is_viral": False,
                "confidence": 0.0,
                "text_length": len(text)
            }
    
    def _sync_predict(self, text: str, threshold: float) -> Dict[str, Any]:
        """Синхронное предсказание (вызывается в отдельном потоке)"""
        from predictor.viral_predictor import predict_viral
        
        result = predict_viral(text, threshold)
        
        confidence = abs(result['probability'] - 0.5) * 2 
        
        return {
            "score": float(result['probability']),
            "is_viral": bool(result['viral']),
            "probability": float(result['probability']),
            "confidence": float(confidence),
            "message": str(result['message']),
            "threshold": float(threshold),
            "original_result": result
        }
    
    async def batch_predict(self, texts: list, threshold: float = 0.5) -> list:
        """Пакетное предсказание"""
        tasks = [self.predict(text, threshold) for text in texts]
        return await asyncio.gather(*tasks)