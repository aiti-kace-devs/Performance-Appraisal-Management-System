from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4


class UserBase(BaseModel):
    name:str
    email:str
    password:str
    reset_password_token:str
    created_at:date

class UserCreate(UserBase):
    name:str
    email:str
    password:str
    reset_password_token:str
    created_at:date

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: UUID4

    class Config:
        orm_mode= True

class UserSchema(UserBase):
    pass