import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase




class User(APIBase):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    staff_id = Column(String,nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)
    reset_password_token = Column(String,nullable=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'),nullable=False)
    created_at = Column(DateTime,default=datetime.UTC, nullable=False)

    appraisals = relationship("Appraisal", back_populates="user")