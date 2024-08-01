from pydantic import UUID4,BaseModel,Field,field_validator
from datetime import datetime,date
from dateutil.parser import parse
from typing import Optional
import uuid



class StaffDeadlineBase(BaseModel):
    appraisal_sections_id: UUID4
    staffs_id: UUID4
    supervisor_id: Optional[UUID4]
    start_date:Optional[date]
    end_date: Optional[date]
    comment: Optional[str]


    # Checking if fields are not empty and also not allowing the word string as value
    @field_validator('appraisal_sections_id', 'staffs_id', 'supervisor_id', 'comment', mode='before')
    def check_non_empty_and_not_string(cls, v, info):
        if isinstance(v, str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty or the word "string"')
        return v
    

    # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('appraisal_sections_id', 'staffs_id', 'supervisor_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(str(v), version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v


    # Checking if start_date and end_date is none, current date will be submitted
    @field_validator('start_date', 'end_date', mode='before')
    def validate_and_convert_date_format(cls, v, info):
        if isinstance(v, date) is None:
            try:
                now = datetime.now()
                return now
            except ValueError:
                raise ValueError(f'\n{info.field_name} must be a valid date format and will be converted to YYYY-MM-DDTHH:MM:SS')
        return v



class StaffDeadlineCreate(StaffDeadlineBase):
    pass



    




class StaffDeadlineUpdate(StaffDeadlineBase):
    pass

class StaffDeadlineInDBBase(StaffDeadlineBase):
    id: UUID4

    class Config:
        orm_mode= True

class StaffDeadlineSchema(StaffDeadlineInDBBase):
    pass