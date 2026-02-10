import uuid
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Enum, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)