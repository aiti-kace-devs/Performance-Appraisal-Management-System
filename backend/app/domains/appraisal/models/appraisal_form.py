import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class appraisal_form(APIBase):
    appraisal_id =  Column(UUID(as_uuid=True), ForeignKey('appraisal.id'),nullable=False)
    appraisal_sections_id =  Column(UUID(as_uuid=True), ForeignKey('appraisal_sections.id'),nullable=False)
    form_fields = JSON
