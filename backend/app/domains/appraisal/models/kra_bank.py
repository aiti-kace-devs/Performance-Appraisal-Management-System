from datetime import datetime, timezone

from db.base_class import APIBase
from sqlalchemy import JSON, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from domains.appraisal.models.department import Department
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.models.staff import Staff 


class KraBank(APIBase):
    department_id = Column(UUID(as_uuid=True), ForeignKey('department.id'), nullable=False)
    appraisal_section_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_section.id'), nullable=False)
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
    focus_area = Column(JSON, nullable=False)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))

    department = relationship('Department', backref=backref('krabanks', uselist=True))
    appraisal_section = relationship('AppraisalSection', backref=backref('krabanks', uselist=True))
    supervisor = relationship('Staff', backref=backref('supervised_krabanks', uselist=True))
