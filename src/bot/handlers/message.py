from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from bot.keyboards.storages.keyboards.reply import reply_keyboards, user_reply_keyboards
from bot.filters.is_navigation_button import IsNavigationButton
from bot.fsm.fsm import StartMenuFSM
from bot.keyboards.buttons.reply import START_MENU_REPLY_BUTTONS
from bot.keyboards.factory.inline import create_course_menu_inline_keyboard

router = Router()

@router.message(IsNavigationButton())
async def reply_pagination_handler(message: Message):
    keyboard_id = user_reply_keyboards.get(message.from_user.id)
    if not keyboard_id:
        return

    kb = reply_keyboards.get(keyboard_id)
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

@router.message(F.text == START_MENU_REPLY_BUTTONS[0].text) # CREATE COURSE
async def create_course(message: Message, state: FSMContext):
    try:
        await state.set_state(StartMenuFSM.waiting_for_course_title)

        await message.answer("Enter course name:")
    except Exception as e:
        await message.answer(f"Error: {e}")

@router.message(F.text == START_MENU_REPLY_BUTTONS[1].text) # CONTINUE COURSE
async def continue_course(message: Message, state: FSMContext):
    try:
        kb = await create_course_menu_inline_keyboard(message.from_user.id)

        await state.set_state(StartMenuFSM.waiting_for_course_to_continue)
        await message.answer("Which course should I continue?", reply_markup=kb.get_keyboard())
    except Exception as e:
        await message.answer(f"Error: {e}")
