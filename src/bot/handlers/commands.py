from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from api.user.add_user import add_user
from ai.model_clients import AuroraAlphaClient

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    add_user(message.from_user.id)

    await message.answer(
f"""Hello, {message.from_user.first_name}!
Welcome to Learnix Bot!
You added to database!
""")

@router.message(Command("ai"))
async def ai_cmd(message: Message):
    try:
        promt = message.text.replace("/ai", "").strip()
        if not promt:
            await message.answer("Please provide a prompt after the command.")
            return
        
        response = AuroraAlphaClient.generate_response(prompt=promt)
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Error: {e}")