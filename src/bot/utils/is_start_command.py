from aiogram.types import Update

def is_start_command(update: Update) -> bool:
    """Check if the message is the /start command"""
    if update.message and update.message.text:
        return update.message.text.startswith("/start")
    return False