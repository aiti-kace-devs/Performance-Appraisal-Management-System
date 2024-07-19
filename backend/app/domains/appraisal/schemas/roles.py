from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4


class RoleBase(BaseModel):
    name:str
    description: Optional[str] = None
    created_at: date

class RoleCreate(RoleBase):
    name:str
    description: Optional[str] = None
    created_at: date

class RoleUpdate(RoleBase):
    pass

class RoleInDBBase(RoleBase):
    id: UUID4

    class Config:
        orm_mode= True

class RoleSchema(RoleBase):
    pass