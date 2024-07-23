from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel, coni 
from pydantic import UUID4


class AppraisalCycleBase(BaseModel):
    name:str
    description: str
    year: int = int

class AppraisalCycleCreate(AppraisalCycleBase):
    name:str
    description: Optional[str] = None
    year: date

class AppraisalCycleUpdate(AppraisalCycleBase):
    pass

class AppraisalCycleInDBBase(AppraisalCycleBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalCycleSchema(AppraisalCycleBase):
    pass