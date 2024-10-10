from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import APIBase
from sqlalchemy.orm import relationship, backref




class CompetencyBank(APIBase):
    created_by = Column(UUID(as_uuid=True), ForeignKey("staffs.id"), nullable=True)
    competency_type = Column(JSON,nullable=False)

    competency_bank_for_staff = relationship('Staff', backref=backref('staff_competency_bank', uselist=True))

    def serialize(self):
        return {
            'created_by':self.created_by,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }