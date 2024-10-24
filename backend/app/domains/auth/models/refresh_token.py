from typing import Any
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from db.base_class import APIBase
from domains.auth.models.users import User

class RefreshToken(APIBase):
        user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), unique=True,nullable=True)
        refresh_token = Column(String)

        users = relationship('User', backref='users', uselist=True)
    
