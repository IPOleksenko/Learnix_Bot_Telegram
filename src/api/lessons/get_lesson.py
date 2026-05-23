from typing import List, Dict
from db.deps import db
from db.models.user import User
from db.models.lessons.themes import Theme
from db.models.lessons.lessons import Lessons


def _parse_lesson_key(name: str) -> int:
    if "_" in name:
        _, numeric = name.split("_", 1)
    else:
        numeric = name
    return int(numeric)


async def get_course_lessons(user_id: int, course_id: int) -> List[Dict]:
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

    lessons = []
    for name, desc in theme.plan.items():
        try:
            lesson_id = _parse_lesson_key(name)
        except (ValueError, IndexError):
            raise Exception(f"Invalid lesson key format: {name}")

        lessons.append({"id": lesson_id, "name": name, "desc": desc})

    return lessons

async def get_this_lesson_is_completed(
    user_id: int,
    course_id: int,
    lessons_id: List[int]
) -> List[bool]:

    session = db()

    lessons = (
        session.query(Lessons.lesson_id, Lessons.is_completed)
        .join(User)
        .filter(
            User.telegram_id == user_id,
            Lessons.theme_id == course_id,
            Lessons.lesson_id.in_(lessons_id)
        )
        .all()
    )

    lessons_map = {
        lesson_id: is_completed
        for lesson_id, is_completed in lessons
    }

    return [
        lessons_map.get(lesson_id, False)
        for lesson_id in lessons_id
    ]