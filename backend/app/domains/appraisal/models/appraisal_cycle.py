from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase





class AppraisalCycle(APIBase):


    name = Column(String, nullable=False) 
    description = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('staffs.id'), nullable=True)

    staffs = relationship("Staff", back_populates="appraisal_cycles")
    appraisal_sections = relationship("AppraisalSection", back_populates="appraisal_cycles")
    


    



