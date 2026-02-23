from typing import List

from db.deps import db
from db.models.user import User
from db.models.lessons.themes import Theme
from api.lessons.get_lesson import get_this_lesson_is_completed

def get_user_courses(user_id: int) -> List[Theme]:
    session = db()
    
    themes = (
        session.query(Theme)
        .join(User)
        .filter(
            User.telegram_id == user_id,
            Theme.is_learning_request == True
        )
        .all()
    )

    if not themes:
        raise Exception("No learning courses found")

    return themes

def get_this_course_is_completed(user_id: int, course_ids: List[int]) -> List[bool]:

    session = db()

    completed_status = []

    for course_id in course_ids:
        theme = session.query(Theme.plan).filter(
            Theme.id == course_id,
            Theme.user_id == session.query(User.id).filter(User.telegram_id == user_id).scalar_subquery()
        ).first()

        if not theme:
            completed_status.append(False)
            continue

        lesson_ids = [int(k) for k in theme.plan.keys()]

        statuses = get_this_lesson_is_completed(user_id, course_id, lesson_ids)

        completed_status.append(all(statuses))

    return completed_status