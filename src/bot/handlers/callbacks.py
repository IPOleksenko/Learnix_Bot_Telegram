from aiogram import Router, F
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot.keyboards.storages.keyboards.inline import inline_keyboards
from bot.fsm.fsm import StartMenuFSM
from bot.keyboards.factory.inline import create_lesson_menu_inline_keyboard
from api.lessons.generate_lesson import generate_lesson
from bot.keyboards.factory.reply import create_start_menu_reply_keyboard
from api.certificate.service import generate_certificate
from db.deps import db
from db.models.lessons.themes import Theme

router = Router()

@router.callback_query(F.data.startswith("page:"))
async def inline_pagination_handler(callback: CallbackQuery):
    if not callback.message:
        return await callback.answer()

    try:
        _, keyboard_id, page = callback.data.split(":")
        page = int(page)
    except ValueError:
        return await callback.answer("Invalid data", show_alert=True)

    kb = inline_keyboards.get(keyboard_id)
    if kb is None:
        return await callback.answer("Keyboard expired", show_alert=True)

    kb.go_to_page(page)

    await callback.message.edit_reply_markup(
        reply_markup=kb.get_keyboard()
    )

    await callback.answer()

@router.callback_query(StartMenuFSM.waiting_for_course_to_continue, F.data.startswith("choose_course:"))
async def process_continue_course(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()

        course_id = int(callback.data.split(":")[1])

        await callback.message.edit_text("Loading your courses...")

        kb = await create_lesson_menu_inline_keyboard(callback.from_user.id, course_id)

        await callback.message.edit_text(
            f"Select lesson: {course_id}",
            reply_markup=kb.get_keyboard(), 
            parse_mode=None
        )

        await state.clear()

    except Exception as e:
        await callback.message.answer(f"Error: {e}", parse_mode=None)

@router.callback_query(F.data.startswith("choose_lesson:"))
async def open_lesson(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()

        if not callback.message:
            return
        
        message = await callback.message.edit_text("Loading lesson...")

        _, course_id_str, lesson_id_str = callback.data.split(":", 2)
        course_id = int(course_id_str)
        lesson_id = int(lesson_id_str)
        user_id = callback.from_user.id

        await state.update_data(
            user_id=user_id,
            course_id=course_id,
            lesson_id=lesson_id
        )
        await state.set_state(StartMenuFSM.waiting_for_lesson_answer)

        lesson = await generate_lesson(user_id=user_id, course_id=course_id, lesson_id=lesson_id)

        message_text = f"""
{lesson.course_theme} - {lesson.lesson_topic}

{lesson.theory}

{lesson.task}
"""
        await message.edit_text(message_text, parse_mode=None)

    except Exception as e:
        await callback.message.answer(f"Error: {str(e)}", parse_mode=None)

@router.callback_query(F.data.startswith("confirmation:"))
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        _, answer = callback.data.split(":")

        data = await state.get_data()
        user_id = data.get("user_id")
        course_id = data.get("course_id")

        if answer == "yes":
            kb = await create_lesson_menu_inline_keyboard(callback.from_user.id, course_id)
            await callback.message.edit_text("Course confirmed", reply_markup=kb.get_keyboard())
            return await state.set_state(StartMenuFSM.waiting_for_course_to_continue)
        elif answer == "no":
            kb = create_start_menu_reply_keyboard(user_id)
            await callback.message.edit_text("Course cancelled")
            await callback.message.answer("Choose your next action", reply_markup=kb.get_keyboard())
            return await state.clear()
        else:
            return callback.message.answer("Invalid choice.")
    except Exception as e:
        return callback.message.answer(f"Error: {str(e)}", parse_mode=None)
    
@router.callback_query(F.data.startswith("generate_certificate:"))
async def generate_certificate_handler(callback: CallbackQuery):
    try:
        session = db()
        
        await callback.answer()

        if not callback.message:
            return
        
        course_id = int(callback.data.split(":")[1])
        user_id = callback.from_user.id

        name = callback.from_user.full_name

        theme_obj = session.query(Theme).filter_by(id=course_id).first()
        if not theme_obj:
            await callback.message.answer("Theme not found.")
            return
        course_name = theme_obj.name

        date = datetime.now().strftime("%Y-%m-%d")

        await callback.message.edit_text("Generating certificate...")

        certificate_bytes = generate_certificate(name, course_name, date)
        file = BufferedInputFile(certificate_bytes.read(), filename="certificate.pdf")

        await callback.message.answer_document(
            document=file,
            caption="Here is your certificate!"
        )

        kb = create_start_menu_reply_keyboard(user_id)
        await callback.message.edit_text("Certificate generated successfully!")
        await callback.message.answer("Choose your next action", reply_markup=kb.get_keyboard())

    except Exception as e:
        await callback.message.answer(f"Error: {str(e)}", parse_mode=None)