from datetime import datetime
from sqlalchemy import Integer, DateTime, Column
from sqlalchemy.orm import relationship
from db.base import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    themes = relationship("Theme", back_populates="user", cascade="all, delete-orphan")
