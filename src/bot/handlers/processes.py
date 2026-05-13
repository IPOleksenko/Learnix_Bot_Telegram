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
    # Send initial message
    sent_message = await message.answer("🔄 Course generation started...")
    title = message.text
    
    # Track status of each model
    model_statuses = {}

    async def on_status_update(status_info):
        """Callback to update message with model status"""
        model_name = status_info["model"]
        status = status_info["status"]
        error = status_info.get("error", "")
        
        # Map status to emoji
        if status == "processing":
            model_statuses[model_name] = f"⏳ {model_name}: Processing..."
        elif status == "success":
            model_statuses[model_name] = f"✅ {model_name}: Complete"
        elif status == "error":
            model_statuses[model_name] = f"❌ {model_name}: {error}"
        
        # Build status message
        status_text = "📊 Course generation status:\n\n"
        for status_line in model_statuses.values():
            status_text += f"{status_line}\n"
        
        try:
            await sent_message.edit_text(status_text)
        except Exception:
            pass  # Silently ignore if edit fails

    try:
        # Generate course using all models
        theme = await generate_course(
            user_id=message.from_user.id, 
            theme=title,
            on_status_update=on_status_update
        )

        if not theme.is_learning_request:
            await sent_message.edit_text(
                "❌ The provided prompt does not seem to be an educational request.",
                parse_mode=None
            )
            return
        
        await state.clear()

        course_plan = "\n".join([
            f"\t{i}. {desc}"
            for i, (name, desc) in enumerate(theme.plan.items())
        ])

        await state.update_data(
            user_id=message.from_user.id,
            course_id=theme.id
        )

        kb = await create_confirmation_inline_keyboard()

        await sent_message.edit_text(
            f"""✨ Course «{theme.name}» created

📚 Course plan:
{course_plan}""",
            reply_markup=kb.get_keyboard(),
            parse_mode=None
        )
    
    except Exception as e:
        await sent_message.edit_text(
            f"❌ Error: {str(e)}",
            parse_mode=None
        )

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
        await sent_message.edit_text(message_text, parse_mode=None)

        if is_correct:
            kb = await create_lesson_menu_inline_keyboard(message.from_user.id, course_id)
            await message.answer("Congratulations! You've completed the lesson.", reply_markup=kb.get_keyboard())
        
            await state.clear()

            
    except Exception as e:
        await message.answer(f"Error: {e}", parse_mode=None)