from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase

class StaffPermission(APIBase):
    staffs_id = Column(UUID(as_uuid= True), nullable=False)
    roles_id = Column(UUID(as_uuid= True), nullable=False)
    permissions_id = Column(UUID(as_uuid= True), nullable=False)
    