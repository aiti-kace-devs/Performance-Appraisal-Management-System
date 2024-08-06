from typing import Any
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase
import uuid 



class Permission(APIBase):
    name = Column(String(255), unique=True, index=True)
    role_permissions = relationship("RolePermission", back_populates="permissions")

