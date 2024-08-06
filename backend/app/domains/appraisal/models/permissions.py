# from typing import Any
# from sqlalchemy import Column, String
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from db.base_class import APIBase
# import uuid 



# class Permission(APIBase):
#     __tablename__ = 'permissions'
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True)
#     name = Column(String, unique=True, index=True, nullable=False)
#     # role_permissions = relationship('RolePermission', back_populates='permission')

#     # roles = relationship(
#     #     'Role',
#     #     secondary='role_permission',
#     #     back_populates='permissions'
#     # )
   

