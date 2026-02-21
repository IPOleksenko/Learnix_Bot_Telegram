from aiogram.filters import BaseFilter
from aiogram.types import Message
from bot.keyboards.storages.keyboards.reply import (
    reply_keyboards,
    user_reply_keyboards,
)

class IsNavigationButton(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        keyboard_id = user_reply_keyboards.get(message.from_user.id)
        if not keyboard_id:
            return False

        kb = reply_keyboards.get(keyboard_id)
        if not kb:
            return False

        return message.text in {kb.prev_button_text, kb.next_button_text}