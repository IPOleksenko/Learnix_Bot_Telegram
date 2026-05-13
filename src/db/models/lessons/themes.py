from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from db.base import Base
from db.mixins.timestamp import TimestampMixin

class AI_Theme_Generation(Base, TimestampMixin):
    __tablename__ = "ai_theme_generation"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    theme_id = Column(Integer, ForeignKey("theme.id"), nullable=False)
    plan_type = Column(String, nullable=False)
    model = Column(String, nullable=False)

    themes = relationship("Theme", back_populates="ai_theme_generation")

class Theme(Base, TimestampMixin):
    __tablename__ = "theme"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    language = Column(String, nullable=False)
    count_lessons = Column(Integer, nullable=False)
    plan_type = Column(String, nullable=False)
    plan = Column(JSON, nullable=False)

    is_learning_request = Column(Boolean, nullable=False, default=True)

    ai_theme_generation = relationship("AI_Theme_Generation", back_populates="themes")
    users = relationship("User", back_populates="theme")
    lessons = relationship("Lessons", back_populates="theme", cascade="all, delete-orphan")
