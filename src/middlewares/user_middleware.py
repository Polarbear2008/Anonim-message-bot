from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from database import db

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any]
    ) -> Any:
        user = await db.get_user(event.from_user.id)
        if not user:
            user = await db.create_user(event.from_user.id)

        data["user"] = user
        return await handler(event, data)