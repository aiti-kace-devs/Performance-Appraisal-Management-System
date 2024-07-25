import datetime
from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class AppraisalSubmission(APIBase):

    appraisals_id = Column(UUID(as_uuid=True))
    staffs_id = Column(UUID(as_uuid=True))
    submitted_values = Column(JSON, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.now(), onupdate= datetime.datetime.now())
    completed_at = Column(DateTime, default=datetime.datetime.now(), onupdate= datetime.datetime.now())
    submitted = Column(Boolean, default=True)
    completed = Column(Boolean, default=True)
    approval_status = Column(Boolean, default=True)
    approval_date = Column(DateTime, default=datetime.datetime.now(), onupdate= datetime.datetime.now())
    appraisal_forms_id = Column(UUID(as_uuid=True))
    comment = Column(String(255), nullable=True)

    #appraisals = relationship("Appraisal", back_populates = "appraisal_submissions")
    #staffs = relationship("Staff", back_populates = "appraisal_submissions")
    #appraisal_forms = relationship("AppraisalForm", back_populates = "appraisal_submissions") 