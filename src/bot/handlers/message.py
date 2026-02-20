from aiogram.types import Message
from aiogram import Router
from bot.keyboards.storages.keyboards.reply import START_MENU_REPLY_KEYBOARDS, USER_START_MENU_REPLY_KEYBOARDS
from bot.filters.is_navigation_button import IsNavigationButton

router = Router()

@router.message(IsNavigationButton())
async def reply_pagination_handler(message: Message):
    keyboard_id = USER_START_MENU_REPLY_KEYBOARDS.get(message.from_user.id)
    if not keyboard_id:
        return

    kb = START_MENU_REPLY_KEYBOARDS.get(keyboard_id)
    if not kb:
        return

    if message.text == kb.prev_button_text:
        kb.previous_page()

    elif message.text == kb.next_button_text:
        kb.next_page()

    else:
        return

    await message.answer(
        "Page switched",
        reply_markup=kb.get_keyboard(),
    )