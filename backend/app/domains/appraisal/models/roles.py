import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase




class Role(APIBase):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True),index=True,primary_key=True, default=uuid.uuid4)
    name = Column(String,nullable=False)
    description = Column(String,nullable=True)
    created_at = Column(DateTime,default=datetime.UTC, nullable=False)

    users = relationship("User",back_populates="role")