import json
from db.models.lessons.lessons import Lessons
from db.models.user import User
from db.deps import db
from ai.model_clients import Clients
from templates.prompts.checking_lesson_prompt import checking_lesson_prompt

def checking_lesson(user_id: int, course_id: int, lesson_id: int, message: str):
    user = db().query(User).filter_by(telegram_id=user_id).first()
    if user is None:
        raise Exception("User not found")
    
    lesson = db().query(Lessons).filter_by(user_id=user.id, theme_id=course_id, lesson_id=lesson_id).first()
    if lesson is None:
        raise Exception("Lesson not found for user")

    prompt = checking_lesson_prompt.substitute(
        assignment=lesson.task,
        answer=message,
        language=lesson.language
    )
    response = Clients["default"].generate_response(prompt=prompt)
    json_response = json.loads(response)
    
    if json_response.get("is_correct", False):
        lesson.is_completed = True
        db().commit()

    return lesson, json_response.get("feedback", "")