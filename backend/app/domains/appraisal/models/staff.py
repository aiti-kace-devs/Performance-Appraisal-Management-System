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



    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "other_name": self.other_name,
            "full_name": f"{self.first_name} {self.last_name}" + (f" {self.other_name}" if self.other_name else ""),
            "position": self.position,
            "email": self.email,
            "department_id": self.department_id,
            "grade": self.grade,
            "appointment_date": self.appointment_date,
        }
