from pydantic import UUID4,BaseModel,field_validator
from datetime import datetime,date
from dateutil.parser import parse
from typing import Optional
import uuid



class StaffBase(BaseModel):
    first_name : str
    last_name : str
    other_name : Optional[str]
    gender : str
    position : str
    user_id : Optional[UUID4]
    department_id : Optional[UUID4]
    grade : str
    appointment_date : Optional[date]


    # Checking if fields are not empty and also not allowing the word string as value
    @field_validator('first_name', 'last_name', 'other_name', 'gender','position', 'grade',  mode='before')
    def check_non_empty_and_not_string(cls,v,info):
        if isinstance(v,str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty "string"') 
        return v


    # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('user_id', 'department_id',  mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(str(v), version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v


    # Checking if start_date and end_date is none, current time and date will be submitted
    @field_validator('appointment_date', mode='before')
    def validate_and_convert_date_format(cls, v, info):
        if v is None:
            try:
                dt = parse(v)
                now = datetime.now()
                combined_datetime = dt.replace(hour=now.hour, minute=now.minute, second=now.second)
                formatted_date = combined_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                return formatted_date
            except ValueError:
                raise ValueError(f'\n{info.field_name} must be a valid date format and will be converted to YYYY-MM-DDTHH:MM:SS')
        return v


class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass

class StaffInDBBase(StaffBase):
    id: UUID4

    class Config:
        orm_mode= True

class StaffSchema(StaffInDBBase):
    pass




