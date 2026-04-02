from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import validates

class SoftDeleteMixin:
    is_active = Column(Boolean, default=True, nullable=False)
    deactivation_reason = Column(String, nullable=True)
    deactivated_at = Column(DateTime(timezone=True), nullable=True)

    @validates("is_active")
    def set_deactivated_at(self, key, value):
        if value is False:
            if self.deactivated_at is None:
                self.deactivated_at = datetime.now(timezone.utc)
        else:
            self.deactivated_at = None
            self.deactivation_reason = None
        return value