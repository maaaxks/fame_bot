# bot/handlers/common.py
from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_menu import main_keyboard
from bot.keyboards.inline import get_inline_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработчик команды /start с клавиатурой"""
    welcome_text = """
🎉 <b>Добро пожаловать в Viral Predictor Bot!</b>

🤖 <i>Я анализирую тексты и предсказываю их виральный потенциал.</i>

📊 <b>Что я умею:</b>
• Анализировать текст на виральность
• Давать оценку вероятности распространения

💡 <b>Выберите действие:</b>
"""
    
    await message.answer(
        welcome_text,
        parse_mode="HTML",
        reply_markup=main_keyboard()  # REPLY клавиатура
    )
    
    # Также отправляем inline-кнопки
    await message.answer(
        "📱 <b>Быстрые действия:</b>",
        parse_mode="HTML",
        reply_markup=get_inline_keyboard()  # INLINE кнопки
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
ℹ️ <b>Помощь по использованию бота</b>

📝 <b>Как это работает:</b>
1. Отправьте мне любой текст (10-5000 символов)
2. Я проанализирую его с помощью ML модели
3. Вы получите детальный отчет

📊 <b>В отчете вы увидите:</b>
• Вероятность вирального распространения
• Уверенность прогноза
• Длину текста

💡 <b>Советы:</b>
• Оптимальная длина: 100-4000 символов
• Избегайте спама и повторений
• Добавляйте эмоциональные слова
• Используйте вопросы для вовлечения

🔧 <b>Команды:</b>
/start - Главное меню
/predict - Анализ текста
/stats - Статус модели
/about - О боте

🎯 <b>Просто отправьте текст или нажмите "Анализ текста"</b>
"""
    
    await message.answer(
        help_text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )

@router.message(Command("about"))
async def cmd_about(message: types.Message):
    """Обработчик команды /about"""
    about_text = """
🤖 <b>Viral Predictor Bot</b>

📈 <i>Бот для предсказания виральности текстовых постов</i>

⚙️ <b>Технологии:</b>
• TensorFlow + Keras нейронная сеть
• Обработка естественного языка (NLP)
• Машинное обучение на основе реальных данных
• Асинхронная архитектура на aiogram

🎯 <b>Возможности:</b>
• Анализ текста на виральный потенциал
• Оценка вероятности распространения

<b>Исходный код:</b>
https://github.com/maaaxks/fame_bot
"""
    
    await message.answer(
        about_text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )

@router.message(lambda message: message.text == "📊 Проанализировать текст")
async def handle_predict_button(message: types.Message, state: FSMContext):
    """Обработка кнопки 'Проанализировать текст'"""
    from bot.handlers.prediction import PredictionState
    from bot.keyboards.main_menu import predict_keyboard
    
    await message.answer(
        "📝 <b>Отправьте текст для анализа виральности</b>\n\n"
        "📏 <i>Оптимальная длина: 10-4000 символов</i>\n\n"
        "💡 <i>Что анализируем:</i>\n"
        "• Вероятность вирального распространения\n"
        "• Длину текста\n"
        "• Уверенность прогноза\n",
        parse_mode="HTML",
        reply_markup=predict_keyboard()  # Специальная клавиатура для анализа
    )
    await state.set_state(PredictionState.waiting_for_text)

@router.message(lambda message: message.text == "ℹ️ Помощь")
async def handle_help_button(message: types.Message):
    """Обработка кнопки 'Помощь'"""
    await cmd_help(message)

@router.message(lambda message: message.text == "🤖 О боте")
async def handle_about_button(message: types.Message):
    """Обработка кнопки 'О боте'"""
    await cmd_about(message)

@router.message(lambda message: message.text == "📈 Статус модели")
async def handle_stats_button(message: types.Message):
    """Обработка кнопки 'Статус модели'"""
    from bot.handlers.prediction import cmd_stats
    await cmd_stats(message)

@router.message(lambda message: message.text == "🔙 Назад в меню")
async def handle_back_button(message: types.Message, state: FSMContext):
    """Обработка кнопки 'Назад в меню'"""
    await state.clear()
    await cmd_start(message)
