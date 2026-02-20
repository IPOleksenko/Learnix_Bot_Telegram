from bot.keyboards.base.reply import ReplyKeyboardBase
from bot.keyboards.buttons.reply import START_MENU_REPLY_BUTTONS
from bot.keyboards.storages.keyboards.reply import START_MENU_REPLY_KEYBOARDS

def create_start_menu_reply_keyboard() -> ReplyKeyboardBase:
    start_menu_reply_buttons_len = len(START_MENU_REPLY_BUTTONS)

    kb = ReplyKeyboardBase(
        buttons=START_MENU_REPLY_BUTTONS,
        row_width=start_menu_reply_buttons_len,
        page_size=start_menu_reply_buttons_len,
        show_page_numbers=False,
    )

    START_MENU_REPLY_KEYBOARDS[kb.keyboard_id] = kb
    return kb