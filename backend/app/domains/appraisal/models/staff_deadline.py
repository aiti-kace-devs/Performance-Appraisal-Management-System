from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class StaffDeadline(APIBase):

    appraisal_sections_id = Column(UUID(as_uuid=True))
    staffs_id = Column(UUID(as_uuid=True))
    supervisor_id = Column(UUID(as_uuid=True))
    start_date = Column(String, nullable=True)
    end_date = Column(String(255), nullable=True)
    comment = Column(String(255), nullable=True)