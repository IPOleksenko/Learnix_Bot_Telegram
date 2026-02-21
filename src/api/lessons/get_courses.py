from typing import List

from db.deps import db
from db.models.user import User
from db.models.lessons.themes import Theme

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