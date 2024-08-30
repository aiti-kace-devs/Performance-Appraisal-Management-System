import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import APIBase




class User(APIBase):
    staff_id = Column(UUID(as_uuid=True),nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=True)
    reset_password_token = Column(String(255),nullable=True)
    role_id = Column(UUID(as_uuid=True))
