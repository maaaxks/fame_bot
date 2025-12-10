# bot/handlers/prediction.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from bot.services.predictor import PredictorService
from bot.config import settings

from bot.keyboards.inline import get_analysis_keyboard
from bot.keyboards.main_menu import main_keyboard
from bot.keyboards.main_menu import predict_keyboard


router = Router()
logger = logging.getLogger(__name__)

predictor = PredictorService(
    model_path=settings.ML_MODEL_PATH,
    tokenizer_path=settings.TOKENIZER_PATH
)

class PredictionState(StatesGroup):
    waiting_for_text = State()

@router.message(Command("predict"))
async def cmd_predict(message: Message, state: FSMContext):
    """Обработчик команды /predict"""
    await message.answer(
        "📝 <b>Отправьте текст для анализа виральности</b>\n\n"
        f"📏 <i>Оптимальная длина: {settings.MIN_TEXT_LENGTH}-{settings.MAX_TEXT_LENGTH} символов</i>\n\n"
        "💡 <i>Что анализируем:</i>\n"
        "• Вероятность стать виральным\n"
        "• Длину текста\n"
        "• Даем рекомендации",
        parse_mode="HTML",
        recply_markup=predict_keyboard()
    )
    await state.set_state(PredictionState.waiting_for_text)

@router.message(F.text == "🔙 Назад в меню")
async def handle_back_to_menu(message: Message, state: FSMContext):
    """Обработка кнопки 'Назад в меню'"""
    await state.clear()
    from bot.handlers.common import cmd_start
    await cmd_start(message)

@router.message(PredictionState.waiting_for_text)
async def process_text(message: Message, state: FSMContext):
    """Обработка текста для предсказания"""
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    text = message.text or ""
    text_length = len(text)

    if text == "🔙 Назад в меню":
        await handle_back_to_menu(message, state)
        return
    
    if text_length < settings.MIN_TEXT_LENGTH:
        await message.answer(
            f"⚠️ Текст слишком короткий. Минимум {settings.MIN_TEXT_LENGTH} символов.\n"
            f"📏 Ваш текст: {text_length} символов"
        )
        return
    
    if text_length > settings.MAX_TEXT_LENGTH:
        await message.answer(
            f"⚠️ Текст слишком длинный. Максимум {settings.MAX_TEXT_LENGTH} символов.\n"
            f"📏 Ваш текст: {text_length} символов"
        )
        return
    
    try:
        result = await predictor.predict(text, settings.VIRAL_THRESHOLD)
        
        response = format_prediction_response(result, text)
        
        await message.answer(
            response, 
            parse_mode="HTML",
            reply_markup=get_analysis_keyboard()  # Inline-кнопки под сообщением
        )
        
        # Дополнительное сообщение с кнопками menu
        await message.answer(
            "🎯 <b>Что дальше?</b>\n\n"
            "Вы можете:\n"
            "• Отправить новый текст для анализа\n"
            "• Вернуться в главное меню\n"
            "• Посмотреть другие примеры",
            parse_mode="HTML",
            reply_markup=main_keyboard()  #Reply-клавиатура
        )

        # Логируем успешное предсказание
        logger.info(f"Предсказание для пользователя {message.from_user.id}: "
                   f"score={result.get('score', 0):.3f}, length={text_length}")
        
    except Exception as e:
        logger.error(f"Ошибка предсказания: {e}")
        await message.answer(
            "❌ <b>Произошла ошибка при анализе</b>\n\n"
            "Попробуйте еще раз или обратитесь к администратору.",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )
    
    
    await state.clear()

def format_prediction_response(result: dict, original_text: str) -> str:
    score = result.get("score", 0.5) * 100
    confidence = result.get("confidence", 0) * 100
    text_length = result.get("text_length", 0)
    
    # Определяем уровень потенциала
    if score < 20:
        level = "📉 Очень низкий виральный потенциал"
        level_emoji = "📉"
    elif score < 40:
        level = "📉 Низкий виральный потенциал"
        level_emoji = "📉"
    elif score < 60:
        level = "📊 Средний виральный потенциал"
        level_emoji = "📊"
    elif score < 80:
        level = "📈 Высокий виральный потенциал"
        level_emoji = "📈"
    else:
        level = "🚀 Очень высокий виральный потенциал"
        level_emoji = "🚀"
    
    # Прогресс-бар
    progress_bar = create_progress_bar(score / 100)
    
    # Рекомендации
    recommendations = get_recommendations(score, text_length, confidence)
    
    # Интерпретация уверенности
    if confidence > 80:
        confidence_text = "🔬 Высокая точность прогноза"
    elif confidence > 50:
        confidence_text = "📊 Средняя точность прогноза"
    else:
        confidence_text = "⚠️ Низкая точность, результат приблизительный"
    
    return f"""
📊 <b>Анализ завершен!</b>

{level_emoji} <b>{level}</b>
{progress_bar}

✅ <b>Вероятность виральности:</b> {score:.1f}%
🎯 <b>Уверенность прогноза:</b> {confidence:.1f}% ({confidence_text})
📏 <b>Длина текста:</b> {text_length} символов



<code>{original_text[:120]}{'...' if len(original_text) > 120 else ''}</code>
"""

def create_progress_bar(percentage: float, length: int = 10) -> str:
    """Создание текстового прогресс-бара"""
    filled = int(percentage * length)
    empty = length - filled
    bar = "█" * filled + "░" * empty
    return f"<code>{bar}</code>"

def get_recommendations(score: float, length: int, is_viral: bool) -> str:
    return

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Статистика модели"""
    if predictor.is_loaded:
        status = "✅ <b>Модель загружена и готова к работе</b>"
    else:
        status = "❌ <b>Модель не загружена</b>"
    
    await message.answer(
        f"🤖 <b>Статистика бота</b>\n\n"
        f"{status}\n"
        f"📁 <b>Модель:</b> {settings.ML_MODEL_PATH}\n"
        f"📁 <b>Токенизатор:</b> {settings.TOKENIZER_PATH}\n"
        f"⚡ <b>Порог виральности:</b> {settings.VIRAL_THRESHOLD}\n"
        f"📏 <b>Длина текста:</b> {settings.MIN_TEXT_LENGTH}-{settings.MAX_TEXT_LENGTH} символов",
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )