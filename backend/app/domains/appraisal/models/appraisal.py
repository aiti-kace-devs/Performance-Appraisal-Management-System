import datetime
from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class Appraisal(APIBase):

    description = Column(Text, nullable=True)
    year = Column(Integer)

    # appraisal_form_sections = relationship("AppraisalSection", backref="appraisal_form_section")
    # submissions = relationship("AppraisalSubmission", backref="app_form_form")


    # appraisal_form_sections = relationship("AppraisalSection", backref="appraisal_form_section")
    # submissions = relationship("AppraisalSubmission", backref="app_form_form")

    # users = relationship("User",back_populates="appraisals")
    # role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), unique=True, nullable=False)
    # roles = relationship("Role",back_populates="appraisals")

