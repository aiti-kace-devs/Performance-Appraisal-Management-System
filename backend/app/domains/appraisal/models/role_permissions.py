from typing import Any
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase
import uuid 



class RolePermission(APIBase):
    __tablename__ = "role_permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, default=uuid.uuid4)

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id"))
    
    roles = relationship("Role", back_populates="role_permissions")
    permissions = relationship("Permission", back_populates="role_permissions")
   
