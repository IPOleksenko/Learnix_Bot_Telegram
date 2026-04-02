from aiogram.types import Update

def get_user_from_update(update: Update):
    """Extract user from any type of update"""
    if update.message:
        return update.message.from_user
    elif update.callback_query:
        return update.callback_query.from_user
    elif update.inline_query:
        return update.inline_query.from_user
    elif update.chosen_inline_result:
        return update.chosen_inline_result.from_user
    elif update.poll_answer:
        return update.poll_answer.user
    elif update.chat_member:
        return update.chat_member.new_chat_member.user
    return None