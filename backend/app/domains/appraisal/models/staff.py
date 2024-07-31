from typing import Any
from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class Staff(APIBase):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    other_name = Column(String, nullable=True)
    gender = Column(String)
    position = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True))
    department_id = Column(UUID(as_uuid=True))
    grade = Column(String(255), nullable=False)
    appointment_date = Column(Date, nullable=True)

    def serialize(self):
        return {
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }