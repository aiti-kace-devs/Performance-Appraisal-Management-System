from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import APIBase
from sqlalchemy.orm import relationship




class CompetencyBank(APIBase):
    appraisal_section_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_sections.id'), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staffs.id'), index=True, nullable=False)
    competency_type = Column(JSON,nullable=False)

    competency_bank_appraisal_section = relationship('AppraisalSection', back_populates='appraisal_section_competency_bank', uselist=False, cascade='all')
    staff_competency_bank = relationship('Staff', back_populates='competency_bank_staff', uselist=False, cascade='all')
