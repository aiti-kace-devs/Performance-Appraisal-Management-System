from typing import Any
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase




class RolePermission(APIBase):
    
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"))
    
    roles = relationship("Role", back_populates="role_permissions")
    permissions = relationship("Permission", back_populates="role_permissions")
   
