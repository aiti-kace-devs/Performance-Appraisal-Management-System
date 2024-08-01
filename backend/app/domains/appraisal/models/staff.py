<<<<<<< HEAD
import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, String, Text,Integer
=======
from typing import Any
from sqlalchemy import Column, Date, String
>>>>>>> 0ab3f152a475199175e363c26417debb069e72b0
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
<<<<<<< HEAD
    appointment_date = Column(Date, nullable=True)
=======
    appointment_date = Column(Date, nullable=True)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }
>>>>>>> 0ab3f152a475199175e363c26417debb069e72b0
