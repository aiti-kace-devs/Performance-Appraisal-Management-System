from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4


class DepartmentBase(BaseModel):
    name:str
    description: Optional[str] = None
    created_at: date

class DepartmentCreate(DepartmentBase):
    name:str
    description: Optional[str] = None
    created_at: date

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentInDBBase(DepartmentBase):
    id: UUID4

    class Config:
        orm_mode= True

class DepartmentSchema(DepartmentBase):
    pass