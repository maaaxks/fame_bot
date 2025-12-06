import asyncio
import logging
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
#from bot.handlers import common, prediction
#from bot.middlewares.throttling import ThrottlingMiddleware

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    bot=Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    #dp.message.middleware(ThrottlingMiddleware())
    
    #dp.include_router(common.router)
    #dp.include_router(prediction.router)
    router=Router() #затычка пока без мл
    dp.include_router(router)

    #await dp.start_polling(bot)

    @router.message(Command("start"))
    async def cmd_start(message: Message):
        logger.info(f"Пользователь {message.from_user.id} нажал /start")
        await message.answer(
            "🎉 <b>Добро пожаловать!</b>\n\n"
            "Я бот для предсказания популярности текстовых постов.\n\n"
            "📊 <b>Что я умею:</b>\n"
            "• Анализировать текст\n"
            "• Предсказывать популярность\n"
            "• Давать рекомендации\n\n"
            "📝 <b>Как использовать:</b>\n"
            "Просто отправь мне любой текст!\n\n"
            "⚡ <i>ML модель скоро будет добавлена...</i>",
            parse_mode="HTML"
        )
    
    # Обработчик команды /help
    @router.message(Command("help"))
    async def cmd_help(message: Message):
        await message.answer(
            "ℹ️ <b>Помощь</b>\n\n"
            "Сейчас бот в режиме разработки.\n"
            "Скоро здесь появится:\n"
            "• Предсказание популярности\n"
            "• Анализ текста\n"
            "• Статистика\n\n"
            "📞 По вопросам: @ваш_username",
            parse_mode="HTML"
        )
    
    # Обработчик команды /about
    @router.message(Command("about"))
    async def cmd_about(message: Message):
        await message.answer(
            "🤖 <b>Fame Predictor Bot</b>\n"
            "Версия: 0.1.0 (альфа)\n"
            "Статус: в разработке\n\n"
            "📈 <i>Скоро будет круто!</i>",
            parse_mode="HTML"
        )
    
    # Обработчик любого текста
    @router.message()
    async def handle_text(message: Message):
        text = message.text or message.caption or ""
        
        if not text.strip():
            await message.answer("📝 Отправьте текст для анализа")
            return
        
        # Простой ответ (пока без ML)
        text_length = len(text)
        
        await message.answer(
            f"📊 <b>Анализ текста:</b>\n\n"
            f"📝 <b>Длина:</b> {text_length} символов\n"
            f"📈 <b>Статус:</b> Анализ отключен\n\n"
            f"🔮 <i>ML модель скоро будет добавлена!</i>\n"
            f"<i>Ваш текст:</i> {text[:50]}...",
            parse_mode="HTML"
        )
    
    # Запуск бота
    logger.info("✅ Бот успешно запущен!")

    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())