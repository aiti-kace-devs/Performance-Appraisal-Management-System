from typing import Any
from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class Staff(APIBase):
    title = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    other_name = Column(String, nullable=True)
    gender = Column(String)
    position = Column(String, nullable=False)
    email = Column(String, unique=True)
    department_id = Column(UUID(as_uuid=True))
    grade = Column(String(255), nullable=False)
    appointment_date = Column(Date, nullable=True)
