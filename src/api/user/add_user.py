from db.deps import db
from db.models.user import User


def add_user(user_id: int) -> User:
    user = db().query(User).filter_by(telegram_id=user_id).first()
    if user:
        return user, "User already exists in the database."
    
    new_user = User(telegram_id=user_id)

    db().add(new_user)
    db().flush()
    db().refresh(new_user)

    return new_user, "User added successfully to database."
