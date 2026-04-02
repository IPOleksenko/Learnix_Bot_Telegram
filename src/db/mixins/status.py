from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import validates

class BlockableMixin:
    deactivation_reason = Column(String, nullable=True)
    deactivated_at = Column(DateTime(timezone=True), nullable=True)

    BLOCKED_STATUS = None

    @validates("status")
    def handle_status_change(self, key, value):
        if self.BLOCKED_STATUS is None:
            raise ValueError("BLOCKED_STATUS must be defined in model")

        if value == self.BLOCKED_STATUS:
            if self.deactivated_at is None:
                self.deactivated_at = datetime.now(timezone.utc)
        else:
            self.deactivated_at = None
            self.deactivation_reason = None

        return value

    @validates("deactivation_reason")
    def validate_reason(self, key, value):
        if self.status == self.BLOCKED_STATUS and not value:
            raise ValueError("deactivation_reason is required when blocked")
        return value