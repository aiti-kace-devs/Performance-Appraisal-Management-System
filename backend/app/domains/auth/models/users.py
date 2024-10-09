from datetime import datetime, timedelta, timezone
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import APIBase
from sqlalchemy.orm import relationship



class User(APIBase):
    staff_id = Column(UUID(as_uuid=True),ForeignKey('staffs.id'), nullable=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=True)
    reset_password_token = Column(String(255),nullable=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime, nullable=True)
    lock_count = Column(Integer, default=0)

    staffs = relationship("Staff", back_populates="users", uselist=True)
    roles = relationship("Role", back_populates="users", uselist=True)

    def is_account_locked(self):
        return self.account_locked_until and self.account_locked_until > datetime.now()
    
    def lock_account(self, lock_time_minutes=10):
        self.account_locked_until = datetime.now() + timedelta(minutes=lock_time_minutes)
        self.failed_login_attempts = 0  # Reset failed attempts after locking

    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.account_locked_until = None