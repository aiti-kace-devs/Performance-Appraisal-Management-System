from typing import Any
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import JSON, Column
from db.base_class import APIBase



class AppraisalForm(APIBase):
    appraisal_id =  Column(UUID(as_uuid=True), ForeignKey('appraisals.id'), unique=True, nullable=False)
    appraisal_sections_id =  Column(UUID(as_uuid=True), ForeignKey('appraisal_sections.id'), unique=True, nullable=False)
    form_fields = Column(JSON, nullable=False)


    appraisal_submissions_form = relationship('AppraisalSubmission', back_populates='appraisal_form_submissions', uselist=False, cascade='all, delete-orphan')
    appraisal_forms_appraisals = relationship('Appraisal', back_populates='appraisal_form_appraisal', uselist=False, cascade='all')
    appraisal_forms_appraisal_section = relationship('AppraisalSection', back_populates='appraisal_section_appraisal_forms', uselist=False, cascade='all')

    