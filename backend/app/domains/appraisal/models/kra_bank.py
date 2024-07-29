from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase
from datetime import datetime, timezone


class KraBank(APIBase):

    department_id = Column(UUID, ForeignKey('department.id'), nullable=False)
    appraisal_section_id = Column(UUID, ForeignKey('appraisal.id'), nullable=False)
    supervisor_id = Column(UUID, ForeignKey('staff.id'), nullable=False)
    focus_area = Column(JSON, nullable=False)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))





   