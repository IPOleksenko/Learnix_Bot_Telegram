from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update
from db.models.user import User
from db.session import SessionLocal


def is_start_command(update: Update) -> bool:
    """Check if the message is the /start command"""
    if update.message and update.message.text:
        return update.message.text.startswith("/start")
    return False

def get_user_id_from_update(update: Update):
    """Extract user_id from any type of update"""
    if update.message:
        return update.message.from_user.id
    elif update.callback_query:
        return update.callback_query.from_user.id
    elif update.inline_query:
        return update.inline_query.from_user.id
    elif update.chosen_inline_result:
        return update.chosen_inline_result.from_user.id
    elif update.poll_answer:
        return update.poll_answer.user.id
    elif update.chat_member:
        return update.chat_member.new_chat_member.user.id
    return None

class IsActiveMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        if is_start_command(event):
            return await handler(event, data)
    
        user_id = get_user_id_from_update(event)
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