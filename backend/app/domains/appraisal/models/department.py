from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class Department(APIBase):

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

<<<<<<< HEAD
    kra_banks = relationship('KraBank', back_populates='department')
=======
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }
>>>>>>> 0ab3f152a475199175e363c26417debb069e72b0
    