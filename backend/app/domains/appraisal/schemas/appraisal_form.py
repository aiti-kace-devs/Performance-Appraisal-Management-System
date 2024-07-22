from pydantic import UUID4,BaseModel,field_validator
from sqlalchemy import JSON
import uuid


class AppraisalFormBase(BaseModel):
    staffs_id : UUID4
    roles_id : UUID4
    form_fields : JSON

class AppraisalFormCreate(BaseModel):
    staffs_id : UUID4
    roles_id : UUID4
    form_fields : JSON
    

    @field_validator('staffs_id', 'roles_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(v, version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v

class AppraisalFormUpdate(AppraisalFormBase):
    pass

class AppraisalFormInDBBase(AppraisalFormBase):
    id: UUID4
    

    class Config:
        orm_mode= True

class AppraisalFormSchema(AppraisalFormBase):
    pass