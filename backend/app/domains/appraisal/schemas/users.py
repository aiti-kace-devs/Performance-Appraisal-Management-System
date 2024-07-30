from datetime import date,time
from typing import Optional, Any, Dict
import uuid

from pydantic import BaseModel, field_validator
from pydantic import UUID4


class UserBase(BaseModel):
    email:str
    password:Optional[str] = None
    reset_password_token:str
    staff_id :  Optional[UUID4]
    role_id :  Optional[UUID4]

    @field_validator('email','reset_password_token' ,mode='before')
    def check_non_empty_and_not_string(cls,v,info):
        if isinstance(v,str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty "string"')
    #make minimum value 1 
        if len(v.strip()) < 1:
            raise ValueError(f'{info.field_name} should have a minimum value of 1')
        return v
    
      # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('role_id', 'staff_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(str(v), version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v

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