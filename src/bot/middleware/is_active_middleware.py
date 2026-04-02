from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware

from db.models.user import User
from db.session import SessionLocal
from aiogram.types import Update
from bot.utils.get_user_from_update import get_user_from_update
from bot.utils.is_start_command import is_start_command

class IsActiveMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        if is_start_command(event):
            return await handler(event, data)
    
        user = get_user_from_update(event)
        user_id = user.id if user else None
        if user_id is None:
            return await handler(event, data)

        with SessionLocal() as session:  
            user = session.query(User).filter(User.telegram_id == user_id).first()

            if not user.is_active:
                if event.message:
                    deactivation_reason = user.deactivation_reason
                    text_user_not_active = f"Your account is not active."
                    if deactivation_reason:
                        text_user_not_active += f"\nDeactivation reason: {deactivation_reason}"

                    await event.message.answer(
                        text_user_not_active
                    )
                elif event.callback_query:
                    await event.callback_query.answer(
                        text_user_not_active
                    )
                return

        return await handler(event, data)