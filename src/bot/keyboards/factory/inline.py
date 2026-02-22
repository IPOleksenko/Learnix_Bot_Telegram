from bot.keyboards.base.inline import InlineKeyboardBase
from bot.keyboards.storages.keyboards.inline import inline_keyboards
from bot.keyboards.buttons.inline import CONFIRMATION_BUTTONS, user_courses_inline_buttons, user_course_lesson_inline_buttons

def create_confirmation_inline_keyboard() -> InlineKeyboardBase:
    kb = InlineKeyboardBase(
        buttons=CONFIRMATION_BUTTONS,
        row_width=2,
    )

    inline_keyboards[kb.keyboard_id] = kb
    return kb

def create_course_menu_inline_keyboard(user_id: int) -> InlineKeyboardBase:
    kb = InlineKeyboardBase(
        buttons=user_courses_inline_buttons(user_id),
        row_width=1,
        page_size=2,
        show_page_numbers=True,
    )

    inline_keyboards[kb.keyboard_id] = kb
    return kb

def create_lesson_menu_inline_keyboard(user_id: int, course_id: int) -> InlineKeyboardBase:
    kb = InlineKeyboardBase(
        buttons=user_course_lesson_inline_buttons(user_id, course_id),
        row_width=1,
        page_size=1,
        show_page_numbers=True,
    )

    inline_keyboards[kb.keyboard_id] = kb
    return kb