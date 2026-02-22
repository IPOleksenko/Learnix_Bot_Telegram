import json

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.keyboards.storages.keyboards.inline import inline_keyboards
from bot.fsm.fsm import StartMenuFSM
from bot.keyboards.factory.inline import create_lesson_menu_inline_keyboard
from api.lessons.generate_lesson import generate_lesson
from bot.keyboards.factory.reply import create_start_menu_reply_keyboard

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

        kb = create_lesson_menu_inline_keyboard(callback.from_user.id, course_id).get_keyboard()

        await callback.message.edit_text(
            f"Select lesson: {course_id}",
            reply_markup=kb
        )

        await state.clear()

    except Exception as e:
        await callback.message.answer(f"Error: {e}")

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

        lesson = generate_lesson(user_id=user_id, course_id=course_id, lesson_id=lesson_id)

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
        }
        json_response = json.dumps(lesson_dict, ensure_ascii=False, indent=2)
        await message.edit_text(json_response)

    except Exception as e:
        await callback.message.answer(f"Error: {str(e)}")

@router.callback_query(F.data.startswith("confirmation:"))
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        _, answer = callback.data.split(":")

        data = await state.get_data()
        user_id = data.get("user_id")
        course_id = data.get("course_id")

        if answer == "yes":
            kb = create_lesson_menu_inline_keyboard(callback.from_user.id, course_id).get_keyboard()
            await callback.message.edit_text("Course confirmed", reply_markup=kb)
            return await state.set_state(StartMenuFSM.waiting_for_course_to_continue)
        elif answer == "no":
            kb = create_start_menu_reply_keyboard(user_id)
            await callback.message.edit_text("Course cancelled")
            await callback.message.answer("Choose your next action", reply_markup=kb.get_keyboard())
            return await state.clear()
        else:
            return callback.message.answer("Invalid choice.")
    except Exception as e:
        return callback.message.answer(f"Error: {str(e)}")