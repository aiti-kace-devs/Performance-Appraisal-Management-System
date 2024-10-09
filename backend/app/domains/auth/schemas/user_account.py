from datetime import date,time, datetime
import sqlalchemy
from typing import Optional, Any, Dict
import uuid
from sqlalchemy import DateTime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic import UUID4



from pydantic import BaseModel
from typing import Optional


class StaffSchema(BaseModel):
    id: Optional[UUID4]
    first_name: str
    last_name: str
    other_name: Optional[str] = None
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


class RoleSchema(BaseModel):
    id: Optional[UUID4]
    name: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email:EmailStr
    password:Optional[str]
    reset_password_token:Optional[str]
    is_active: bool = True
    failed_login_attempts: int 
    account_locked_until: Optional[datetime]
    lock_count: Optional[int]
    staff: Optional[StaffSchema] 
    role: Optional[RoleSchema]

    class Config:
        orm_mode = True


    @field_validator('email','reset_password_token' ,mode='before')
    def check_non_empty_and_not_string(cls,v,info):
        if isinstance(v,str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty "string"')
    #make minimum value 1 
        return v

      # Checking if UUID4 fields accept only UUID4 as value
    # @field_validator('staff_id', mode='before')
    # def validate_fields_with_uuid4(cls, v, info):
    #     try:
    #         uuid.UUID(str(v), version=4)
    #     except ValueError:
    #         raise ValueError(f'\n{info.field_name} must have a valid UUID4')
    #     return v

class UserCreate(UserBase):
    pass



class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: UUID4

    class Config:
        orm_mode= True

class UserSchema(UserInDBBase):
    pass