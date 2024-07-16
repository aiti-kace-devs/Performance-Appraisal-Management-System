from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4


class AppraisalFormBase(BaseModel):
    name:str
    description: Optional[str] = None
    created_at: date

class AppraisalFormCreate(AppraisalFormBase):
    name:str
    description: Optional[str] = None
    created_at: date

class AppraisalFormUpdate(AppraisalFormBase):
    pass

class AppraisalFormInDBBase(AppraisalFormBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalFormSchema(AppraisalFormBase):
    pass