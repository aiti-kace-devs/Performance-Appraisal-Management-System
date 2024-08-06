import datetime
from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, DECIMAL, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class Appraisal(APIBase):

    appraisal_cycles_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_cycles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staffs.id', ondelete='CASCADE', onupdate='CASCADE'), index=True, nullable=False)
    supervisor_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    overall_score = Column(DECIMAL(precision=10, scale=2), nullable=False, index=True, default=0.00)


    appraisal_form_appraisal = relationship('AppraisalForm', back_populates='appraisal_forms_appraisals', uselist=False, cascade='all, delete-orphan')
    app_appraisal_submission = relationship('AppraisalSubmission', back_populates='appraisal_app_submissions', uselist=False, cascade='all, delete-orphan')


    # users = relationship("User",back_populates="appraisals")
    # role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), unique=True, nullable=False)
    # roles = relationship("Role",back_populates="appraisals")

