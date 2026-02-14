import json
from db.models.user import User
from db.models.lessons.lessons import Lessons
from db.models.lessons.themes import Theme

from db.deps import db

from ai.model_clients import AuroraAlphaClient

from templates.promts.generate_lesson_prompt import generate_lesson_prompt

def generate_lesson(user_id: int, course_id: int, lesson_id: int):
    user = db().query(User).filter_by(telegram_id=user_id).first()
    if user is None:
        raise Exception("User not found")
    
    theme = db().query(Theme).filter_by(user_id=user.id, id=course_id).first()
    if theme is None:
        raise Exception("Theme not found for user")
    
    if lesson_id > theme.count_lessons:
        raise Exception("Invalid lesson ID for the given theme")
    
    lesson = db().query(Lessons).filter_by(user_id=user.id, theme_id=theme.id, lesson_id=lesson_id).first()
    if lesson:
        return lesson

    language = theme.language
    course_theme = theme.name
    plan = theme.plan

    lesson_key = f"{lesson_id}"
    if lesson_key not in plan:
        raise Exception(f"Lesson {lesson_key} not found in theme plan")

    current_lesson = plan[lesson_key]

    promt = generate_lesson_prompt.substitute(
        language=language,
        course_theme=course_theme,
        lesson_topic=current_lesson
    )
    
    response = AuroraAlphaClient.generate_response(prompt=promt)
    json_response = json.loads(response)

    lesson = Lessons(
        user_id=user.id,
        theme_id=theme.id,
        lesson_id=lesson_id,
        language=language,
        course_theme=course_theme,
        lesson_topic=current_lesson,
        theory=json_response.get("theory", None),
        task=json_response.get("task", None),
        is_complated=False,
    )

    db().add(lesson)
    db().commit()
    db().refresh(lesson)

    return lesson
    