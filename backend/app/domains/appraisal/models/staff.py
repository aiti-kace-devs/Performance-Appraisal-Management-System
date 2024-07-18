import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class staff(APIBase):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    other_name = Column(String, nullable=True)
    gender = Column(String)
    position = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'),nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey('department.id'),nullable=False)
    grade = Column(String)
    #appointment_date = Column(String)
