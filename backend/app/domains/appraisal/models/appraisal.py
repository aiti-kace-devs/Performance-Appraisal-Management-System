import datetime
from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class Appraisal(APIBase):

<<<<<<< HEAD
    appraisal_cycles_id = Column(UUID(as_uuid=True))
    staffs_id = Column(UUID(as_uuid=True))
    supervisor_id = Column(UUID(as_uuid=True))
    overall_score = Column(String(255), nullable=False)
=======
    description = Column(Text, nullable=True)
    year = Column(Integer)

    # appraisal_form_sections = relationship("AppraisalSection", backref="appraisal_form_section")
    # submissions = relationship("AppraisalSubmission", backref="app_form_form")



>>>>>>> GIKPA-252-Create-appraisal-form-repo-service-and-API
