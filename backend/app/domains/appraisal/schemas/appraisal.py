from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4


class AppraisalBase(BaseModel):
     appraisal_cycles_id:UUID4
     staffs_id: UUID4
     supervisor_id: UUID4
     overall_score: str

class AppraisalCreate(AppraisalBase):
    appraisal_cycles_id:UUID4
    staffs_id: UUID4
    supervisor_id: UUID4
    overall_score: str

class AppraisalUpdate(AppraisalBase):
    pass

class AppraisalInDBBase(AppraisalBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSchema(AppraisalBase):
    pass