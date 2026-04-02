from enum import Enum
from db.deps import db
from db.models.user import User

class UserAlreadyExistsEnum(str, Enum):
    exists = "User already exists in the database."
    updated = "User already exists in the database, but language was updated."
    added = "User added successfully to database."

async def add_user(user) -> User:
    session = db()

    user_id = user.id
    user_language = user.language_code

    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user:
        if user.language != user_language:
            user.language = user_language
            session.commit()
            session.refresh(user)
            return user, UserAlreadyExistsEnum.updated.value
        return user, UserAlreadyExistsEnum.exists.value
    
    new_user = User(telegram_id=user_id, language=user_language)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user, UserAlreadyExistsEnum.added.value
