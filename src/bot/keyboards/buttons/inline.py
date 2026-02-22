from aiogram.types import InlineKeyboardButton
from api.lessons.get_courses import get_user_courses
from api.lessons.get_lesson import get_course_lessons

CONFIRMATION_BUTTONS = [
    InlineKeyboardButton(text="YES", callback_data="confirmation:yes"),
    InlineKeyboardButton(text="NO", callback_data="confirmation:no")
]

user_courses_inline_buttons = lambda user_id: [
    InlineKeyboardButton(
        text=course.name,
        callback_data=f"choose_course:{course.id}"
    )
    for course in get_user_courses(user_id)
]

user_course_lesson_inline_buttons = lambda user_id, course_id: [
    InlineKeyboardButton(
        text=f"{lesson['name']}. {lesson['desc']}",
        callback_data=f"choose_lesson:{course_id}:{lesson['name']}"
    )
    for i, lesson in enumerate(get_course_lessons(user_id, course_id))
]

