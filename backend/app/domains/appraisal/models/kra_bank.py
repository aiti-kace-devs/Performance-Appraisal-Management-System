from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase
from datetime import datetime, timezone

from domains.appraisal.models.department import Department
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.models.staff import Staff 


class KraBank(APIBase):

    department_id = Column(UUID, ForeignKey('department.id'), nullable=False)
    appraisal_section_id = Column(UUID, ForeignKey('appraisal.id'), nullable=False)
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey('staff.id'), nullable=False)
    focus_area = Column(JSON, nullable=False)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))

    supervisor = relationship('Staff', back_populates='kra_banks')
    department = relationship('Department', back_populates='kra_banks')
    appraisal_section = relationship('AppraisalSection', back_populates='kra_banks')





   