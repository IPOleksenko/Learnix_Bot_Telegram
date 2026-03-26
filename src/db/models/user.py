from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Integer, DateTime, Column, String
from sqlalchemy.orm import relationship
from db.base import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)

    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    deactivation_reason = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    themes = relationship("Theme", back_populates="user", cascade="all, delete-orphan")
