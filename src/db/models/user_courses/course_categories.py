from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base
from db.models.user_courses.user_courses import course_category_link
from db.mixins.timestamp import TimestampMixin

class CourseCategory(Base, TimestampMixin):
    __tablename__ = "course_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    courses = relationship(
        "UserCourse",
        secondary=course_category_link,
        back_populates="categories"
    )