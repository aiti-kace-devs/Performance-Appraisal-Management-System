from sqlalchemy import JSON, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase



class appraisal_form(APIBase):
    appraisal_id =  Column(UUID(as_uuid=True))
    appraisal_sections_id =  Column(UUID(as_uuid=True))
    form_fields = JSON
