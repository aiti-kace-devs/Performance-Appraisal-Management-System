from pydantic import UUID4,BaseModel,field_validator, EmailStr,Field
from datetime import datetime,date
from dateutil.parser import parse
from typing import Optional, Any, Dict , List
import uuid
from enum import Enum
from domains.appraisal.schemas.department import DepartmentInDBBase


class Gender(str, Enum):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'

class Title(str, Enum):
    Mr = 'Mr.'
    Mrs = 'Mrs.'
    Prof = 'Prof.'
    Dr = 'Dr.'
    Ms = 'Ms.'
    Miss = 'Miss'
    Ing = 'Ing.'
    Rev = 'Rev.'
    #Rev.Dr = 'Rev.Dr.'
    Bishop = 'Bishop.'
    Other = 'Other'

class PermissionSchema(BaseModel):
    id: UUID4
    name: str

class RoleSchema(BaseModel):
    id: UUID4
    name: str
    permissions: List[PermissionSchema]

class PermissionResponse(BaseModel):
    id: int
    name: str
    codename: str

class StaffResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str
    permissions: List[PermissionResponse]

    class Config:
        orm_mode = True
        
class StaffBase(BaseModel):
    title: Title
    first_name : str
    last_name : str
    other_name : Optional[str]
    gender : Gender
    email: EmailStr
    position : str
    department_id : UUID4
    grade : str
    appointment_date : Optional[date]
    # role_id : Optional[UUID4] = Field(None, exclude=True)
    role_id: UUID4
    


    # Checking if fields are not empty and also not allowing the word string as value
    @field_validator('title', 'first_name', 'last_name', 'gender','email', 'position', 'grade',  mode='before')
    def check_non_empty_and_not_string(cls,v,info):
        if isinstance(v,str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty "string"') 
        return v


    # Checking if UUID4 fields accept only UUID4 as value
    @field_validator( 'department_id',  mode='before')
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




class StaffInDBBase(BaseModel):
    id: UUID4
    title: Title
    first_name : str
    last_name : str
    other_name : str
    gender : Gender
    email: EmailStr
    position : str
    department_id : str
    grade : str
    appointment_date : Optional[date]

    class Config:
        orm_mode= True
        


class DepartmentInfo(BaseModel):
    id: UUID4
    name: str

class RoleInfo(BaseModel):
    id: UUID4
    name: str


class StaffWithFullNameInDBBase(BaseModel):
    id: UUID4
    title: Title
    first_name : str
    last_name : str
    other_name : str
    full_name : str
    gender : Gender
    email: EmailStr
    position : str
    department_id : DepartmentInfo
    grade : str
    appointment_date : Optional[date]
    role_id: RoleInfo

    class Config:
        orm_mode= True


class StaffSchema(StaffInDBBase):
    pass



class StaffCreate(StaffBase):
    pass