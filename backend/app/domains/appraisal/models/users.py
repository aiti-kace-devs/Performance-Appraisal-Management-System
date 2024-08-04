import datetime
from typing import Any
import uuid
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase




# class User(APIBase):
#     staff_id = Column(String,nullable=False)
#     email = Column(String, nullable=False)
#     password = Column(String, nullable=True)
#     reset_password_token = Column(String,nullable=True)
#     # role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'),nullable=False)


#     # roles = relationship("Role",back_populates="users")
#     appraisals = relationship("Appraisal", back_populates="users")


class User(APIBase):
    __tablename__ = 'users'  # Added table name definition
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    staff_id = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)
    reset_password_token = Column(String, nullable=True)
    # role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), nullable=False)
    # role = relationship("Role", back_populates="users")
    # appraisals = relationship("Appraisal", back_populates="users")