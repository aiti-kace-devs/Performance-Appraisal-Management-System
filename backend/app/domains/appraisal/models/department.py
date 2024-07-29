from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class Department(APIBase):

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    kra_banks = relationship('KraBank', back_populates='department')
    