from pydantic import UUID4,BaseModel,field_validator
from sqlalchemy import JSON
import uuid
from typing import Dict, Any


class AppraisalFormBase(BaseModel):
    appraisal_id : UUID4
    appraisal_sections_id : UUID4
    form_fields : Dict[str, Any]

    @field_validator('appraisal_id', 'appraisal_sections_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(str(v), version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v

    @staticmethod
    def validate_appriasal_form(value: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(value, dict) or not value:
            raise ValueError('form_fields type must not be a an empty valid JSON object')
        return value

class AppraisalFormCreate(AppraisalFormBase):
    pass



    

class AppraisalFormUpdate(AppraisalFormBase):
    pass

class AppraisalFormInDBBase(AppraisalFormBase):
    id: UUID4


    class Config:
        orm_mode= True

class AppraisalFormSchema(AppraisalFormInDBBase):
    pass