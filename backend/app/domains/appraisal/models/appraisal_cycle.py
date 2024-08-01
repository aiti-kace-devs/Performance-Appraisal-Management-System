from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase





class AppraisalCycle(APIBase):


    name = Column(String, unique=True, nullable=False) 
    description = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    


    



