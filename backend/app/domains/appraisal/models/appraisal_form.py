from typing import Any
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import JSON, Column,ForeignKey
from db.base_class import APIBase



class AppraisalForm(APIBase):
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staffs.id'), nullable=True)
    appraisal_sections_id =  Column(UUID(as_uuid=True), ForeignKey('appraisal_sections.id'), nullable=True) #
    form_fields = Column(JSON, nullable=False)

    staffs = relationship("Staff", back_populates="appraisal_forms")
    #appraisal_sections = relationship("AppraisalSection", back_populates="appraisal_forms")
