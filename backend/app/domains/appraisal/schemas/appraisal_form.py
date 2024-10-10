from pydantic import UUID4,BaseModel,field_validator
from sqlalchemy import JSON
import uuid
from typing import Dict, Any,List,Optional



class RaedAppraisalSectionBase(BaseModel):
    id: Optional[UUID4]
    name: Optional[str]
    description: Optional[str]
    appraisal_year: Optional[int]




class ReadAppraisalFormBase(BaseModel):
    created_by: Optional[UUID4]
    appraisal_sections: Optional[RaedAppraisalSectionBase]
    form_fields : List[Any]



class AppraisalFormBase(BaseModel):
    appraisal_sections_id : UUID4
    form_fields : List[Any]


class AppraisalFormCreate(AppraisalFormBase):
    pass



    @field_validator('appraisal_sections_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(v, version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v

    # @staticmethod
    # def validate_appriasal_form(value: Dict[str, Any]) -> Dict[str, Any]:
    #     if not isinstance(value, dict) or not value:
    #         raise ValueError('form_fields type must not be a an empty valid JSON object')
    #     return value

class AppraisalFormUpdate(AppraisalFormBase):
    pass

class AppraisalFormInDBBase(ReadAppraisalFormBase):
    id: UUID4


    class Config:
        orm_mode= True

class AppraisalFormSchema(AppraisalFormInDBBase):
    pass