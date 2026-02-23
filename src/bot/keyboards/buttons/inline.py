from aiogram.types import InlineKeyboardButton
from api.lessons.get_courses import get_this_course_is_completed, get_user_courses
from api.lessons.get_lesson import get_course_lessons, get_this_lesson_is_completed

CONFIRMATION_BUTTONS = [
    InlineKeyboardButton(text="YES", callback_data="confirmation:yes"),
    InlineKeyboardButton(text="NO", callback_data="confirmation:no")
]

async def user_courses_inline_buttons(user_id: int) -> list[InlineKeyboardButton]:
    courses = await get_user_courses(user_id)
    course_ids = [course.id for course in courses]

    statuses = await get_this_course_is_completed(user_id, course_ids)

    buttons = []
    for course, is_completed in zip(courses, statuses):
        prefix = "✅ " if is_completed else ""
        buttons.append(
            InlineKeyboardButton(
                text=f"{prefix}{course.name}",
                callback_data=f"choose_course:{course.id}"
            )
        )

    return buttons

async def user_course_lesson_inline_buttons(user_id: int, course_id: int) -> list[InlineKeyboardButton]:
    lessons = await get_course_lessons(user_id, course_id)

    lesson_ids = [int(lesson["name"]) for lesson in lessons]

    statuses = await get_this_lesson_is_completed(
        user_id=user_id,
        course_id=course_id,
        lessons_id=lesson_ids
    )

    buttons = []

    for lesson, is_completed in zip(lessons, statuses):
        prefix = "✅ " if is_completed else ""

        buttons.append(
            InlineKeyboardButton(
                text=f"{prefix}{lesson['name']}. {lesson['desc']}",
                callback_data=f"choose_lesson:{course_id}:{lesson['name']}"
            )
        )

    return buttons

