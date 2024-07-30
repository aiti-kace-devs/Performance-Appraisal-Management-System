from datetime import date,time
from typing import Optional, Any, Dict
import uuid

from pydantic import BaseModel, UUID4, Field, field_validator, root_validator


class AppraisalBase(BaseModel):
     appraisal_cycles_id:UUID4
     staffs_id: UUID4
     supervisor_id: UUID4
     overall_score: str

class AppraisalCreate(AppraisalBase):
    appraisal_cycles_id:UUID4
    staffs_id: UUID4
    supervisor_id: UUID4
    overall_score: Optional[str]


     # Checking if fields are not empty and also not allowing the word string as value
    @root_validator('appraisal_cycles_id', 'supervisor_id', 'staffs_id', 'overall_score', mode='before')
    def check_non_empty_and_not_string(cls, value, info):
        if isinstance(value, str) and (value.strip() == '' or value.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty or the word "string"')
        return value
    

     # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('appraisal_cycles_id', 'staffs_id', 'supervisor_id', mode='before')
    def validate_fields_with_uuid4(cls, value, info):
        try:
            uuid.UUID(value, version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return value



class AppraisalUpdate(AppraisalBase):
    pass

class AppraisalInDBBase(AppraisalBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSchema(AppraisalBase):
    pass