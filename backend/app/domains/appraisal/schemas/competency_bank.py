from datetime import date,time
from typing import Optional, Any, Dict
import uuid

from pydantic import BaseModel, field_validator
from pydantic import UUID4
from sqlalchemy import JSON


class CompentencyBankBase(BaseModel):
    appraisal_section_id : Optional[UUID4]
    staff_id : Optional[UUID4]
    compentency_type : Dict[str,Any]

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

class CompentencyBankCreate(CompentencyBankBase):
    pass



class CompentencyBankUpdate(CompentencyBankBase):
    pass

class CompentencyBankInDBBase(CompentencyBankBase):
    id: UUID4

    class Config:
        orm_mode= True

class CompentencyBankSchema(CompentencyBankBase):
    pass