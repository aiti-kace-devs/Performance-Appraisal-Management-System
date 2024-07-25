from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel, Field, field_validator
from pydantic import UUID4


class DepartmentBase(BaseModel):
    name:str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    name:str
    description: Optional[str] = Field(None, min_length=1)


@field_validator('name','description', mode='before')
def check_non_empty_and_not_string(cls,v,info):
    if isinstance(v,str) and (v.strip() == '' or v.strip().lower() == 'string'):
        raise ValueError(f'\n{info.field_name} should not be empty "string"')

        #make minimum value 1
    if len(v.strip()) < 1:
        raise ValueError(f'{info.field_name} should have a minimum value of 1')

    return v




class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentInDBBase(DepartmentBase):
    id: UUID4

    class Config:
        orm_mode= True

class DepartmentSchema(DepartmentBase):
    pass