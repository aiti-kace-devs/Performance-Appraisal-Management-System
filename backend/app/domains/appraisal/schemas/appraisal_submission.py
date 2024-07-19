from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4
from sqlalchemy import JSON


class AppraisalSubmissionBase(BaseModel):
    appraisals_id : UUID4 
    staffs_id : UUID4
    submitted_values : JSON
    started_at : date
    completed_at : date
    submitted : bool
    completed : bool
    approval_status : bool
    approval_date : date
    appraisal_forms_id : UUID4
    comment : str

class AppraisalSubmissionCreate(AppraisalSubmissionBase):
    appraisals_id : UUID4 
    staffs_id : UUID4
    submitted_values : JSON
    started_at : date
    completed_at : date
    submitted : bool
    completed : bool
    approval_status : bool
    approval_date : date
    appraisal_forms_id : UUID4
    comment : str

class AppraisalSubmissionUpdate(AppraisalSubmissionBase):
    pass

class AppraisalSubmissionInDBBase(AppraisalSubmissionBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSubmissionSchema(AppraisalSubmissionBase):
    pass