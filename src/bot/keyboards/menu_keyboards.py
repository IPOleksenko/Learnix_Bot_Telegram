from aiogram.types import (
    KeyboardButton,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from aiogram import Router, F
from aiogram.filters import Command

from bot.keyboards.base.reply import ReplyKeyboardBase
from bot.keyboards.base.inline import InlineKeyboardBase

router = Router()

# ================================================================
# STORAGE
# ================================================================

# INLINE
INLINE_KEYBOARDS: dict[str, InlineKeyboardBase] = {}

# REPLY
REPLY_KEYBOARDS: dict[str, ReplyKeyboardBase] = {}
USER_REPLY_KEYBOARD: dict[int, str] = {}


# ================================================================
# INLINE KEYBOARD FACTORY
# ================================================================

def create_simple_inline_keyboard() -> InlineKeyboardBase:
    buttons = [
        InlineKeyboardButton(text=f"Button {i}", callback_data=f"item:{i}")
        for i in range(1, 21)
    ]

    kb = InlineKeyboardBase(
        buttons=buttons,
        row_width=2,
        page_size=4,
        show_page_numbers=True,
    )

    INLINE_KEYBOARDS[kb.keyboard_id] = kb
    return kb


# ================================================================
# REPLY KEYBOARD FACTORY
# ================================================================

def create_simple_reply_keyboard() -> ReplyKeyboardBase:
    buttons = [
        KeyboardButton(text=f"Button {i}")
        for i in range(1, 21)
    ]

    kb = ReplyKeyboardBase(
        buttons=buttons,
        row_width=2,
        page_size=4,
        show_page_numbers=True,
    )

    REPLY_KEYBOARDS[kb.keyboard_id] = kb
    return kb


# ================================================================
# COMMANDS
# ================================================================

@router.message(Command("inline"))
async def cmd_inline(message: Message):
    kb = create_simple_inline_keyboard()

    await message.answer(
        "Inline keyboard:",
        reply_markup=kb.get_keyboard(),
    )


@router.message(Command("reply"))
async def cmd_reply(message: Message):
    kb = create_simple_reply_keyboard()

    USER_REPLY_KEYBOARD[message.from_user.id] = kb.keyboard_id

    await message.answer(
        "Reply keyboard:",
        reply_markup=kb.get_keyboard(),
    )


# ================================================================
# INLINE PAGINATION HANDLER
# ================================================================

@router.callback_query(F.data.startswith("page:"))
async def inline_pagination_handler(callback: CallbackQuery):
    _, keyboard_id, page = callback.data.split(":")

    kb = INLINE_KEYBOARDS.get(keyboard_id)
    if not kb:
        await callback.answer("Keyboard expired", show_alert=True)
        return

    kb.go_to_page(int(page))

    await callback.message.edit_reply_markup(
        reply_markup=kb.get_keyboard()
    )
    await callback.answer()


# ================================================================
# REPLY PAGINATION HANDLER
# ================================================================

@router.message()
async def reply_pagination_handler(message: Message):
    keyboard_id = USER_REPLY_KEYBOARD.get(message.from_user.id)
    if not keyboard_id:
        return

    kb = REPLY_KEYBOARDS.get(keyboard_id)
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
