from typing import Any
from sqlalchemy import Column, Date, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase
from enum import Enum


class Gender(Enum):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'

class Title(Enum):
    Mr = 'Mr.'
    Mrs = 'Mrs.'
    Prof = 'Prof.'
    Dr = 'Dr.'
    Ms = 'Ms.'
    Other = 'Other'


class Staff(APIBase):
    title = Column(String, default=Title, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    other_name = Column(String, nullable=True)
    gender = Column(String, default=Gender, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=False)
    grade = Column(String(255), nullable=False)
    appointment_date = Column(Date, nullable=True)

    user = relationship('User', backref='staffs', uselist=False, cascade='all, delete-orphan')
    

    