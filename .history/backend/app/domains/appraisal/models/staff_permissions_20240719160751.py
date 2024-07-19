from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase

class Staff_Permissions(APIBase):
    
    staff_id = Column(UUID(as_uuid=True), nullable=False)
    roles_id = Column(UUID(as_uuid=True), nullable=False)
    permissions_id = Column(UUID(as_uuid=True), nullable=False)
    


