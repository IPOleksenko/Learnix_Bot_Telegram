import json
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from api.user.add_user import add_user

from bot.keyboards.factory.reply import create_start_menu_reply_keyboard

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    user = message.from_user
    user, user_result_text = await add_user(user)

    kb = create_start_menu_reply_keyboard(user.id)

    message_text = f"""
Hello, {message.from_user.first_name}!
Welcome to Learnix Bot!
{user_result_text}
"""
    await message.reply(message_text, reply_markup=kb.get_keyboard())