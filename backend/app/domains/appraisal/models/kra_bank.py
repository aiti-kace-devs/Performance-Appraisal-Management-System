from datetime import datetime, timezone
from db.base_class import APIBase
from sqlalchemy import JSON, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref



class KraBank(APIBase):
    department_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("staffs.id"), nullable=True)
    focus_area = Column(JSON, nullable=False)

    department = relationship('Department', backref=backref('krabanks', uselist=True))
    krabank_for_staff = relationship('Staff', backref=backref('staff_krabanks', uselist=True))
