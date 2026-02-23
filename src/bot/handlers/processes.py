import json

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.fsm.fsm import StartMenuFSM
from api.lessons.generate_course import generate_course
from api.lessons.checking_lesson import checking_lesson
from bot.keyboards.factory.inline import create_confirmation_inline_keyboard, create_lesson_menu_inline_keyboard

router = Router()

@router.message(StartMenuFSM.waiting_for_course_title)
async def process_course_title(message: Message, state: FSMContext):
    try:
        sent_message = await message.answer("Course is generated")
        title = message.text

        theme = await generate_course(user_id=message.from_user.id, lesson_theme=title)

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

        kb = await create_confirmation_inline_keyboard()

        await sent_message.edit_text(f"""
Course «{theme.name}» created

Course plan:
{course_plan}
""", reply_markup=kb.get_keyboard())
        
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
    
        lesson, is_correct, feedback = await checking_lesson(user_id=user_id, course_id=course_id, lesson_id=lesson_id, message=message.text)

        if feedback:
            feedback_text = f"Feedback:\n{feedback}\n\n"
        else:
            feedback_text = "No feedback available.\n\n"

        message_text = f"""
{lesson.course_theme} - {lesson.lesson_topic}

{feedback_text}
"""
        await sent_message.edit_text(message_text)

        if is_correct:
            kb = await create_lesson_menu_inline_keyboard(message.from_user.id, course_id)
            await message.answer("Congratulations! You've completed the lesson.", reply_markup=kb.get_keyboard())
        
            await state.clear()

            
    except Exception as e:
        await message.answer(f"Error: {e}")