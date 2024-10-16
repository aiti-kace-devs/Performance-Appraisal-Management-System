from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase





class AppraisalSection(APIBase):

    #sections = Column(JSON, nullable=False)
    name = Column(String, nullable=False) 
    description = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('staffs.id'), nullable=True)
    appraisal_year = Column(Integer, nullable=True)
    appraisal_cycle_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_cycles.id'), nullable=True)
    

    staffs = relationship("Staff", back_populates="appraisal_sections")
    appraisal_forms = relationship("AppraisalForm", back_populates="appraisal_sections")
    appraisal_cycles = relationship("AppraisalCycle", back_populates="appraisal_sections")
    
    



