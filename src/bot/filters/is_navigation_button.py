from aiogram.filters import BaseFilter
from aiogram.types import Message
from bot.keyboards.storages.keyboards.reply import (
    START_MENU_REPLY_KEYBOARDS,
    USER_START_MENU_REPLY_KEYBOARDS,
)

class IsNavigationButton(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        keyboard_id = USER_START_MENU_REPLY_KEYBOARDS.get(message.from_user.id)
        if not keyboard_id:
            return False

        kb = START_MENU_REPLY_KEYBOARDS.get(keyboard_id)
        if not kb:
            return False

        return message.text in {kb.prev_button_text, kb.next_button_text}