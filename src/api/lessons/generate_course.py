import json
from db.models.user import User
from db.models.lessons.themes import Theme

from db.deps import db

from ai.model_clients import Clients

from templates.prompts.generate_course_prompt import generate_course_prompt

def generate_course(user_id: int, lesson_theme: str):

    user = db().query(User).filter_by(telegram_id=user_id).first()
    if user is None:
        raise Exception("User not found")
    
    prompt = generate_course_prompt.substitute(lesson_theme=lesson_theme)
    response = Clients["default"].generate_response(prompt=prompt)
    json_response = json.loads(response)

    theme = Theme(
        user_id=user.id,
        name=json_response.get("theme", lesson_theme),
        language=json_response.get("detected_language", "unknown"),
        count_lessons=json_response.get("count_lessons", 0),
        plan_type=json_response.get("plan_type", "unknown"),
        plan=json_response.get("plan", []),
        is_learning_request=json_response.get("is_learning_request", True)
    )
    db().add(theme)
    db().commit()
    db().refresh(theme)

    return theme