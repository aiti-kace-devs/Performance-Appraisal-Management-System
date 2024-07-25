from datetime import date,time
from typing import Optional, Any, Dict
import uuid

from pydantic import BaseModel, field_validator
from pydantic import UUID4
from sqlalchemy import JSON


class Compentency_BankBase(BaseModel):
    appraisal_section_id = Optional[UUID4]
    staff_id = Optional[UUID4]
    compentency_type = JSON

class Compentency_BankCreate(Compentency_BankBase):
    appraisal_section_id = Optional[UUID4]
    staff_id = Optional[UUID4]
    compentency_type = JSON

     # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('appraisal_sections_id', 'staffs_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(v, version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v
    
    @staticmethod
    def validate_competency_type(value: Dict[str, Any]) -> Dict[str, Any]:
         if not isinstance(value, dict) or not value:
            raise ValueError('Competency type must be a non-empty valid JSON object')
         return value


class Compentency_BankUpdate(Compentency_BankBase):
    pass

class Compentency_BankInDBBase(Compentency_BankBase):
    id: UUID4

    class Config:
        orm_mode= True

class Compentency_BankSchema(Compentency_BankBase):
    pass