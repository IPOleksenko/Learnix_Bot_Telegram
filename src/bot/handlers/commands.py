import json
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from api.user.add_user import add_user

from api.lessons.generate_course import generate_course

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    add_user(message.from_user.id)

    return await message.answer(
f"""Hello, {message.from_user.first_name}!
Welcome to Learnix Bot!
You added to database!
""")

@router.message(Command("generate_course"))
async def ai_cmd(message: Message):
    try:
        promt = message.text.replace("/generate_course", "").strip()
        if not promt:
            return await message.answer("Please provide a prompt after the command.")
        
        theme = generate_course(user_id=message.from_user.id, lesson_theme=promt)

        if not theme.is_learning_request:
            return await message.answer("The provided prompt does not seem to be an educational request.")
        
        theme_dict = {
            'id': theme.id,
            'user_id': theme.user_id,
            'name': theme.name,
            'language': theme.language,
            'count_lessons': theme.count_lessons,
            'plan_type': theme.plan_type,
            'plan': theme.plan,
            'created_at': str(theme.created_at) if hasattr(theme, 'created_at') else None
        }
            
        json_response = json.dumps(theme_dict, ensure_ascii=False, indent=2)
        
        return await message.answer(json_response)
    
    except Exception as e:
        return await message.answer(f"Error: {e}")