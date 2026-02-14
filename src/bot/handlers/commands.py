import json
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from api.user.add_user import add_user

from api.lessons.generate_course import generate_course
from api.lessons.generate_lesson import generate_lesson

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


@router.message(Command("generate_lesson"))
async def generate_lesson_cmd(message: Message):
    try:
        args = message.text.replace("/generate_lesson", "").strip().split()
        
        if len(args) != 2:
            return await message.answer("Please provide exactly 2 arguments: course ID and lesson ID.")
        
        course_id_str, lesson_id_str = args

        if not course_id_str.isdigit() or not lesson_id_str.isdigit():
            return await message.answer("Both course ID and lesson ID must be numbers.")
        
        course_id = int(course_id_str)
        lesson_id = int(lesson_id_str)

        lesson = generate_lesson(user_id=message.from_user.id, course_id=course_id, lesson_id=lesson_id)
        
        lesson_dict = {
            'id': lesson.id,
            'user_id': lesson.user_id,
            'theme_id': lesson.theme_id,
            'lesson_id': lesson.lesson_id,
            'language': lesson.language,
            'course_theme': lesson.course_theme,
            'lesson_topic': lesson.lesson_topic,
            'theory': lesson.theory,
            'task': lesson.task,
            'is_complated': lesson.is_complated,
            'created_at': str(lesson.created_at) if hasattr(lesson, 'created_at') else None
        }
        
        json_response = json.dumps(lesson_dict, ensure_ascii=False, indent=2)

        return await message.answer(json_response)
    
    except Exception as e:
        return await message.answer(f"Error: {e}")
