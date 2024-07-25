from typing import Any
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase
import uuid 



class Permission(APIBase):
    __tablename__ = "permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid.uuid4)
    name = Column(String(255), unique=True, index=True)
    role_permissions = relationship("RolePermission", back_populates="permissions")

    user_roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
        #overlaps="role_permissions, user_roles, permissions"
        
    )
