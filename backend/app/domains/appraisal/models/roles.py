import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase




class Role(APIBase):
    name = Column(String(255),nullable=False)
    description = Column(String(255),nullable=True)

    users = relationship("User",back_populates="roles")