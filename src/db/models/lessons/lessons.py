from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base

class Lessons(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    theme_id = Column(Integer, ForeignKey("theme.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    theme = relationship("Theme", back_populates="lessons")
