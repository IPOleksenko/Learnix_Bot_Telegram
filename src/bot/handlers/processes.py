import json

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.fsm.fsm import StartMenuFSM
from api.lessons.generate_course import generate_course
from api.lessons.checking_lesson import checking_lesson
from bot.keyboards.factory.inline import create_confirmation_inline_keyboard

router = Router()

@router.message(StartMenuFSM.waiting_for_course_title)
async def process_course_title(message: Message, state: FSMContext):
    try:
        sent_message = await message.answer("The training course is generated")
        title = message.text

        theme = generate_course(user_id=message.from_user.id, lesson_theme=title)

        if not theme.is_learning_request:
            return await message.answer("The provided prompt does not seem to be an educational request.")
        
        await state.clear()

        course_plan = "\n".join([
            f"\t{i+1}. {desc}"
            for i, (name, desc) in enumerate(theme.plan.items())
        ])

        await state.update_data(
            user_id=message.from_user.id,
            course_id=theme.id
        )

        kb = create_confirmation_inline_keyboard().get_keyboard()

        await sent_message.edit_text(f"""
Course «{theme.name}» created

Course plan:
{course_plan}
""", reply_markup=kb)
        
    except Exception as e:
        await message.answer(f"Error: {e}")

@router.message(StartMenuFSM.waiting_for_lesson_answer)
async def process_lesson_answer(message: Message, state: FSMContext):
    try:
        sent_message = await message.answer("The task is being checked")

        data = await state.get_data()
        user_id = data.get("user_id")
        course_id = data.get("course_id")
        lesson_id = data.get("lesson_id")
    
        lesson, feedback = checking_lesson(user_id=user_id, course_id=course_id, lesson_id=lesson_id, message=message.text)

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
            'is_completed': lesson.is_completed,
            'created_at': str(lesson.created_at) if hasattr(lesson, 'created_at') else None,
            'feedback': feedback
        }
        json_response = json.dumps(lesson_dict, ensure_ascii=False, indent=2)

        await sent_message.edit_text(json_response)

        await state.clear()
    except Exception as e:
        await message.answer(f"Error: {e}")