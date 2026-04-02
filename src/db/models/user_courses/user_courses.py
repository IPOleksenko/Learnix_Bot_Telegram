from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship, validates

from db.base import Base
from db.enums.user_courses import CourseLevelEnum, UserCourseStatusEnum
from db.mixins.status import BlockableMixin
from db.mixins.timestamp import TimestampMixin
from db.mixins.uuid import UUIDMixin
from db.utils.languages import validate_languages


course_category_link = Table(
    "course_category_link",
    Base.metadata,
    Column("course_id", ForeignKey("user_courses.id"), primary_key=True),
    Column("category_id", ForeignKey("course_categories.id"), primary_key=True),
)

class UserCourse(Base, UUIDMixin, BlockableMixin, TimestampMixin):
    __tablename__ = "user_courses"

    BLOCKED_STATUS = UserCourseStatusEnum.blocked

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    status = Column(
        SqlEnum(UserCourseStatusEnum, name="user_course_status_enum"),
        default=UserCourseStatusEnum.draft,
        nullable=False
    )

    is_paid = Column(Boolean, default=False, nullable=False)
    is_premium = Column(Boolean, default=False, nullable=False, index=True)

    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=True)

    language = Column(ARRAY(String), nullable=False)
    price = Column(Integer, nullable=False, default=0)

    level = Column(
        SqlEnum(CourseLevelEnum, name="course_level_enum"),
        nullable=False
    )

    users = relationship("User", back_populates="user_courses")
    categories = relationship(
        "CourseCategory",
        secondary=course_category_link,
        back_populates="courses"
    )

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_non_negative"),
        CheckConstraint(
            "(status != 'blocked') OR (deactivated_at IS NOT NULL AND deactivation_reason IS NOT NULL)",
            name="check_course_deactivation"
        ),
    )

    @validates("language")
    def validate_languages(self, key, value):
        return validate_languages(value)