# bot/middlewares/throttling.py
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import time

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.users = {}  # user_id: last_message_time

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        # Проверяем, был ли недавно запрос от пользователя
        if user_id in self.users:
            time_passed = current_time - self.users[user_id]
            if time_passed < self.rate_limit:
                # Слишком частый запрос
                await event.answer(
                    "⏳ Слишком много запросов. Пожалуйста, подождите немного."
                )
                return

        self.users[user_id] = current_time

        return await handler(event, data)