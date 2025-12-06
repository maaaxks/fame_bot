import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Глобальные переменные для загруженных объектов
_model = None
_tokenizer = None


def load_model_and_tokenizer(model_path, tokenizer_path):
    """
    Загружает модель и токенизатор (вызвать один раз при старте)

    Args:
        model_path: путь к файлу модели .h5
        tokenizer_path: путь к файлу токенизатора .pkl
    """
    global _model, _tokenizer

    try:
        _model = tf.keras.models.load_model(model_path)
        print(f" Модель загружена из {model_path}")
    except Exception as e:
        raise Exception(f"Ошибка загрузки модели: {e}")

    try:
        with open(tokenizer_path, 'rb') as f:
            _tokenizer = pickle.load(f)
        print(f"Токенизатор загружен из {tokenizer_path}")
    except Exception as e:
        raise Exception(f"Ошибка загрузки токенизатора: {e}")


def predict_viral(text, threshold=0.5):
    global _model, _tokenizer

    # Проверка загрузки
    if _model is None or _tokenizer is None:
        raise Exception("Сначала вызовите load_model_and_tokenizer()")

    # Очистка текста
    text = str(text).strip()
    if not text:
        raise ValueError("Текст не может быть пустым")

    cleaned_text = ' '.join(text.lower().split())

    sequence = _tokenizer.texts_to_sequences([cleaned_text])

    padded = pad_sequences(sequence, maxlen=200, padding='post', truncating='post')

    probability = float(_model.predict(padded, verbose=0)[0][0])

    is_viral = probability > threshold

    if is_viral:
        if probability > 0.8:
            message = "ВЫСОКАЯ вероятность стать виральным!"
        else:
            message = "Может стать виральным"
    else:
        if probability < 0.3:
            message = "Маловероятно, что станет виральным"
        else:
            message = "Средние шансы на виральность"

    return {
        'viral': is_viral,
        'probability': probability,
        'text_sample': text[:100] + '...' if len(text) > 100 else text,
        'message': message,
        'threshold': threshold
    }


def predict_viral_simple(text):
    """
    Упрощенная версия: возвращает только True/False

    Args:
        text (str): текст Reddit поста

    Returns:
        bool: True если виральный, False если нет
    """
    result = predict_viral(text)
    return result['viral']


def predict_viral_score(text):
    """
    Возвращает только числовую оценку (0-1)

    Args:
        text (str): текст Reddit поста

    Returns:
        float: вероятность виральности от 0 до 1
    """
    result = predict_viral(text)
    return result['probability']
