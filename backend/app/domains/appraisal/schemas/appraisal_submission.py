from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4


class AppraisalSubmissionBase(BaseModel):
    name:str
    description: Optional[str] = None
    created_at: date

class AppraisalSubmissionCreate(AppraisalSubmissionBase):
    name:str
    description: Optional[str] = None
    created_at: date

class AppraisalSubmissionUpdate(AppraisalSubmissionBase):
    pass

class AppraisalSubmissionInDBBase(AppraisalSubmissionBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSubmissionSchema(AppraisalSubmissionBase):
    pass