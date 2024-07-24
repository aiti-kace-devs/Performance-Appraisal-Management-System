from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase





class Compentency_Bank(APIBase):
    appraisal_section_id = Column(UUID(as_uuid=True), nullable=False)
    staff_id = Column(UUID(as_uuid=True), nullable=False)
    compentency_type = Column(JSON,nullable=False)
    

    compentency_banks = relationship("AppraisalCycle", back_populates="staff")