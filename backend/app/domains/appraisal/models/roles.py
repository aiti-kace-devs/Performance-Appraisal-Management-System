import datetime
from typing import Any
import uuid
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from db.base_class import APIBase



    
class Role(APIBase):
     
    
    name = Column(String, unique=True, index=True, nullable=False)
    # permissions = relationship('Permission', back_populates='roles')

    # permissions = relationship(
    #     'Permission',
    #     secondary= "role_permission", 
    #     back_populates='roles'
    # )
    
    # role_permissions = relationship("RolePermission", back_populates="roles")
    # permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
    