from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel, Field, field_validator, UUID4


class DepartmentBase(BaseModel):
    name:str
    description: Optional[str] = None

    @field_validator('name', 'description', mode='before')
    def check_non_empty_and_not_string(cls, v, info):
        if isinstance(v, str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty or the word "string"')
        return v

class DepartmentCreate(DepartmentBase):
    pass



class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentInDBBase(DepartmentBase):
    id: UUID4

    class Config:
        orm_mode= True

class DepartmentSchema(DepartmentInDBBase):
    pass