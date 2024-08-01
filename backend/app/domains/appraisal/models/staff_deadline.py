from typing import Any
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class StaffDeadline(APIBase):

    appraisal_sections_id = Column(UUID(as_uuid=True), ForeignKey('appraisal_sections.id'), nullable=False)
    staffs_id = Column(UUID(as_uuid=True), ForeignKey('staffs.id'), index=True, nullable=False)
    supervisor_id = Column(UUID(as_uuid=True))
    start_date = Column(DateTime, nullable=True)
    end_date = Column(Date, nullable=True)
    comment = Column(String(255), nullable=True) 

    appraisal_section_staff_deadline = relationship("AppraisalSection", back_populates = "staff_deadline_appraisal_section", uselist=False, cascade='all')


    