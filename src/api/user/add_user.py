from db.deps import db
from db.models.user import User


def add_user(user_id: int) -> User:

    if db().query(User).filter_by(telegram_id=user_id).first():
        return
    
    new_user = User(telegram_id=user_id)

    db().add(new_user)
    db().flush()
    db().refresh(new_user)

    return new_user
