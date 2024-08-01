import domains.appraisal.schemas
from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase





class AppraisalSection(APIBase):

    appraisal_cycles_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_cycles.id'), unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False) 
    description = Column(Text, nullable=True)
    

    appraisal_section_appraisal_forms = relationship('AppraisalForm', back_populates='appraisal_forms_appraisal_section', uselist=False, cascade='all, delete-orphan')
    appraisal_section_competency_bank = relationship('CompetencyBank', back_populates='competency_bank_appraisal_section', uselist=False, cascade='all, delete-orphan')
    staff_deadline_appraisal_section = relationship("StaffDeadline", back_populates = "appraisal_section_staff_deadline", uselist=False, cascade='all, delete-orphan')
    
    



