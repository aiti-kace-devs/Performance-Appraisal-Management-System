from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase

class Staff_Permissions(APIBase):

    staff_id = UUID
    roles_id = UUID
    permissions_id = Column()


