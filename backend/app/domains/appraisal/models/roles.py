import datetime
from typing import Any
import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase




class Role(APIBase):
    name = Column(String(255), unique=True, index=True)
    role_permissions = relationship("RolePermission", back_populates="roles")
    users = relationship("User", back_populates="roles")
   

    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        #overlaps="role_permissions, role,permission"
    )
    


