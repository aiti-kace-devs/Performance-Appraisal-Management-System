from datetime import date,time
from typing import Optional, Any, Dict
import uuid

from pydantic import BaseModel, field_validator
from pydantic import UUID4
from sqlalchemy import JSON


class CompetencyBankBase(BaseModel):
    appraisal_section_id : UUID4
    staff_id : UUID4
    competency_type : Dict[str,Any]

    # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('appraisal_section_id', 'staff_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(str(v), version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v
    @staticmethod
    def validate_competency_type(value: Dict[str, Any]) -> Dict[str, Any]:
         if not isinstance(value, dict) or not value:
            raise ValueError('Competency type must be a non-empty valid JSON object')
         return value

class CompetencyBankCreate(CompetencyBankBase):
    pass



class CompetencyBankUpdate(CompetencyBankBase):
    pass

class CompetencyBankInDBBase(CompetencyBankBase):
    id: UUID4

    class Config:
        orm_mode= True

class CompetencyBankSchema(CompetencyBankInDBBase):
    pass