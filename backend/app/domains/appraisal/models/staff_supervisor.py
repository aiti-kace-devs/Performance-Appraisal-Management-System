import datetime
from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


class StaffSupervisor(APIBase):

    appraisal_year = Column(Integer, nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staffs.id'), nullable=True)
    supervisor_id = Column(UUID(as_uuid=True), nullable=True)

    staffs = relationship("Staff", back_populates="staff_supervisors")

