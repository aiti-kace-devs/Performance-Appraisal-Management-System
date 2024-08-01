import datetime
from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class AppraisalSubmission(APIBase):

    appraisals_id = Column(UUID(as_uuid=True), ForeignKey('appraisals.id'), nullable=False)
    staffs_id = Column(UUID(as_uuid=True), ForeignKey('staffs.id'), index=True, nullable=False)
    appraisal_forms_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_forms.id'), nullable=False)
    submitted_values = Column(JSON, nullable=True)
    started_at = Column(Date)
    completed_at = Column(Date)
    approval_date = Column(Date)
    submitted = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    approval_status = Column(String)
    comment = Column(String(255), nullable=True)

    appraisal_app_submissions = relationship("Appraisal", back_populates = "app_appraisal_submission", uselist=False, cascade='all')
    appraisal_form_submissions = relationship("AppraisalForm", back_populates = "appraisal_submissions_form", uselist=False, cascade='all') 