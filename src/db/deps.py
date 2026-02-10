from sqlalchemy.orm import Session
from db.context import db_context


def db() -> Session:
    return db_context.get()
