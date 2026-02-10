from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from api.user.add_user import add_user

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    add_user(message.from_user.id)

    await message.answer(
f"""Hello, {message.from_user.first_name}!
Welcome to Learnix Bot!
You added to database!
""")