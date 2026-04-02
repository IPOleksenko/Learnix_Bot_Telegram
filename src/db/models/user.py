from sqlalchemy import BigInteger, CheckConstraint, Integer, DateTime, Column, String, Enum as SqlEnum
from sqlalchemy.orm import relationship

from db.base import Base
from db.enums.user import UserRoleEnum
from db.mixins.soft_delete import SoftDeleteMixin
from db.mixins.timestamp import TimestampMixin
from db.mixins.uuid import UUIDMixin


class User(Base, UUIDMixin, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    language = Column(String, nullable=False)
    role = Column(
        SqlEnum(UserRoleEnum, name="user_role_enum"),
        default=UserRoleEnum.user,
        nullable=False
    )

    premium_until = Column(DateTime(timezone=True), nullable=True)
    points = Column(Integer, default=0, nullable=False)
    note = Column(String, nullable=True)

    theme = relationship("Theme", back_populates="users", cascade="all, delete-orphan")
    user_courses = relationship("UserCourse", back_populates="users", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("points >= 0", name="check_points_non_negative"),
        CheckConstraint(
            "(is_active = true AND deactivated_at IS NULL AND deactivation_reason IS NULL) "
            "OR (is_active = false AND deactivated_at IS NOT NULL)",
            name="check_active_deactivation_fields"
        ),
    )

    @property
    def is_premium(self) -> bool:
        from datetime import datetime, timezone
        return bool(
            self.premium_until and 
            self.premium_until > datetime.now(timezone.utc)
        )