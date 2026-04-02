from aiogram import BaseMiddleware
from aiogram.types import Update

from api.user.add_user import add_user
from bot.utils.get_user_from_update import get_user_from_update

class EnsureUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        
        user = get_user_from_update(event)
        
        if user:
            db_user, _ = await add_user(user)
            data["db_user"] = db_user

        return await handler(event, data)