from typing import Any
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import JSON, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class Appraisal_form(APIBase):
    appraisal_id =  Column(UUID(as_uuid=True))
    appraisal_sections_id =  Column(UUID(as_uuid=True))
    form_fields = Column(JSON, nullable=False)

    def serialize(self):
        return {
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }