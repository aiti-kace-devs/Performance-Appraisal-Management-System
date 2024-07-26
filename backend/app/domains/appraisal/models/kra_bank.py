from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase
import datetime


class KraBank(APIBase):

    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    appraisal_id = Column(Integer, ForeignKey('appraisal.id'), nullable=False)
    supervisor_id = Column(Integer, ForeignKey('supervisor.id'), nullable=False)
    focus_area = Column(JSON, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now(datetime.UTC))





   