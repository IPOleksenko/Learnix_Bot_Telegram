from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base

class Lessons(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    theme_id = Column(Integer, ForeignKey("theme.id"), nullable=False)
    lesson_id = Column(Integer, nullable=False)

    language = Column(String, nullable=False)
    course_theme = Column(String, nullable=False)
    lesson_topic = Column(String, nullable=False)
    theory = Column(String, nullable=True)
    task = Column(String, nullable=True)
    is_complated = Column(Boolean, nullable=False, default=False)    

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    theme = relationship("Theme", back_populates="lessons")
