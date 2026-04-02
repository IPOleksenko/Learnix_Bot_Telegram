import enum


class UserCourseStatusEnum(enum.Enum):
    draft = "draft"     # course is being created or edited, not visible to users
    pending = "pending" # course is awaiting approval
    active = "active"   # course is published and visible to users
    blocked = "blocked" # course is blocked

class CourseLevelEnum(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"