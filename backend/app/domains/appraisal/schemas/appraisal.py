from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel, UUID4
from pydantic import UUID4


class AppraisalBase(BaseModel):
    name:str
    description: Optional[str] = None
    created_at: date

class AppraisalCreate(AppraisalBase):
    name:str
    description: Optional[str] = None
    created_at: date

class AppraisalUpdate(AppraisalBase):
    pass

class AppraisalInDBBase(AppraisalBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSchema(AppraisalBase):
    pass