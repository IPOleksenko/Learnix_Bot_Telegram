from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.storages.keyboards.inline import INLINE_KEYBOARDS

router = Router()

@router.callback_query(F.data.startswith("page:"))
async def inline_pagination_handler(callback: CallbackQuery):
    if not callback.message:
        return await callback.answer()

    try:
        _, keyboard_id, page = callback.data.split(":")
        page = int(page)
    except ValueError:
        return await callback.answer("Invalid data", show_alert=True)

    kb = INLINE_KEYBOARDS.get(keyboard_id)
    if kb is None:
        return await callback.answer("Keyboard expired", show_alert=True)

    kb.go_to_page(page)

    await callback.message.edit_reply_markup(
        reply_markup=kb.get_keyboard()
    )

    await callback.answer()