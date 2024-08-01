from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase





class AppraisalSection(APIBase):

    appraisal_cycles_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_cycles.id'), unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False) 
    description = Column(Text, nullable=True)
    

    #appraisal_sections = relationship("AppraisalCycle", backref="appraisal_cycles")
    
    



