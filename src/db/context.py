from contextvars import ContextVar
from sqlalchemy.orm import Session

db_context: ContextVar[Session] = ContextVar("db_context")
