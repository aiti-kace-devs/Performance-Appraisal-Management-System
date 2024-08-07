# import datetime
# from typing import Any
# import uuid
# from sqlalchemy import Column, String, ForeignKey, Table
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship, declarative_base
# from db.base_class import APIBase



    
# class Role(APIBase):   
    
#     name = Column(String(255), unique=True, index=True)
#     role_permissions = relationship(
#         "RolePermission", back_populates="role")
#     permissions = relationship(
#         "RolePermission",
#         back_populates="roles",
#         cascade="all, delete-orphan"
#     )