from dateutil.parser import parse
from datetime import date, datetime,time
from typing import Optional, Any, Dict
import uuid

from pydantic import BaseModel, Field, field_validator
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
    comment : str = Field(..., min_length=1)



 # Checking if fields are not empty and also not allowing the word string as value
    @field_validator('appraisals_id', 'staffs_id', 'appraisal_forms_id', 'submitted_values', 'submitted', 'completed', 'approval_status', 'comment', mode='before')
    def check_non_empty_and_not_string(cls, v, info):
        if isinstance(v, str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty or the word "string"')
        return v


    # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('appraisals_id', 'staffs_id', 'appraisal_forms_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(v, version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v


    # Checking if started_at and Completed_at is none, current time nad date will be submitted
    @field_validator('started_at', 'Completed_at', 'approval_date', mode='before')
    def validate_and_convert_date_format(cls, v, info):
        if v is not None:
            try:
                dt = parse(v)
                now = datetime.now()
                combined_datetime = dt.replace(hour=now.hour, minute=now.minute, second=now.second)
                formatted_date = combined_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                return formatted_date
            except ValueError:
                raise ValueError(f'\n{info.field_name} must be a valid date format and will be converted to YYYY-MM-DDTHH:MM:SS')
        return v


class AppraisalSubmissionUpdate(AppraisalSubmissionBase):
    pass

class AppraisalSubmissionInDBBase(AppraisalSubmissionBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSubmissionSchema(AppraisalSubmissionBase):
    pass