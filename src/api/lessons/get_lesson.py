from typing import List, Dict
from db.deps import db
from db.models.user import User
from db.models.lessons.themes import Theme


def get_course_lessons(user_id: int, course_id: int) -> List[Dict]:
    session = db()

    theme = (
        session.query(Theme)
        .join(User)
        .filter(
            User.telegram_id == user_id,
            Theme.id == course_id
        )
        .first()
    )

    if theme is None:
        raise Exception("Course not found")

    lessons = [
        {"name": name, "desc": desc} for name, desc in theme.plan.items()
    ]

    return lessons