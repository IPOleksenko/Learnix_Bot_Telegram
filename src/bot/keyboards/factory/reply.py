from bot.keyboards.base.reply import ReplyKeyboardBase
from bot.keyboards.buttons.reply import START_MENU_REPLY_BUTTONS
from bot.keyboards.storages.keyboards.reply import reply_keyboards
from bot.keyboards.storages.keyboards.reply import user_reply_keyboards

def create_start_menu_reply_keyboard(user_id: int) -> ReplyKeyboardBase:
    start_menu_reply_buttons_len = len(START_MENU_REPLY_BUTTONS)

    kb = ReplyKeyboardBase(
        buttons=START_MENU_REPLY_BUTTONS,
        row_width=start_menu_reply_buttons_len,
        page_size=start_menu_reply_buttons_len,
        show_page_numbers=False,
    )

    reply_keyboards[kb.keyboard_id] = kb
    user_reply_keyboards[user_id] = kb.keyboard_id
    return kb