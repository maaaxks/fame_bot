# bot/main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import settings
from bot.handlers import common, prediction
from bot.middlewares.throttling import ThrottlingMiddleware

async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Проверка токена
    if not settings.BOT_TOKEN or settings.BOT_TOKEN == "your_bot_token_here":
        logger.error("❌ BOT_TOKEN не установлен! Создайте файл .env")
        return
    
    # Проверка модели
    import os
    if not os.path.exists(settings.ML_MODEL_PATH):
        logger.warning(f"⚠️ Модель не найдена по пути: {settings.ML_MODEL_PATH}")
    if not os.path.exists(settings.TOKENIZER_PATH):
        logger.warning(f"⚠️ Токенизатор не найден по пути: {settings.TOKENIZER_PATH}")
    
    # Инициализация бота
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.message.middleware(ThrottlingMiddleware())
    
    dp.include_router(common.router)
    dp.include_router(prediction.router)
    
    logger.info("🤖 Бот запускается...")
    logger.info(f"📁 Модель: {settings.ML_MODEL_PATH}")
    logger.info(f"👤 Админы: {settings.ADMIN_IDS}")
    
    # /start 
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        await message.answer(
            "🤖 <b>Добро пожаловать в Viral Predictor Bot!</b>\n\n"
            "📊 Я анализирую тексты и предсказываю их виральный потенциал.\n\n"
            "📝 <b>Команды:</b>\n"
            "/predict - анализ текста\n"
            "/stats - статус модели\n"
            "/help - помощь\n"
            "/about - о боте\n\n"
            "⚡ <i>Просто отправьте мне текст для анализа!</i>",
            parse_mode="HTML"
        )
    
    #Обработчик /help
    @dp.message(Command("help"))
    async def cmd_help(message: Message):
        await message.answer(
            "ℹ️ <b>Помощь по использованию бота:</b>\n\n"
            "1. Используйте команду <code>/predict</code>\n"
            "2. Отправьте текст для анализа\n"
            "3. Получите детальный отчет\n\n"
            "📊 <b>В отчете вы увидите:</b>\n"
            "• Вероятность виральности\n"
            "• Длину текста\n"
            "• Рекомендации по улучшению\n\n"
            "💡 <b>Советы:</b>\n"
            "• Оптимальная длина: 100-3000 символов\n"
            "• Избегайте спама и повторений",
            parse_mode="HTML"
        )
    
    logger.info("✅ Бот успешно запущен!")
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())