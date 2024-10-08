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

    appraisal_cycles_staff = relationship("Staff", back_populates="staff_appraisal_cycles")
    


    



