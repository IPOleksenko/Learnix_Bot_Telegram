from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from db.base import Base

class Theme(Base):
    __tablename__ = "theme"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)
    language = Column(String, nullable=False)
    count_lessons = Column(Integer, nullable=False)
    plan_type = Column(String, nullable=False)
    plan = Column(JSON, nullable=False)

    is_learning_request = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="themes")
    lessons = relationship("Lessons", back_populates="theme", cascade="all, delete-orphan")
