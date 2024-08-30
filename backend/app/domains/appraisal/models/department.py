from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class Department(APIBase):

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }
    