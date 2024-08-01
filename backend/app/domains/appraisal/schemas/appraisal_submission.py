from dateutil.parser import parse
from datetime import date, datetime,time
from typing import Annotated, Optional, Any, Dict
import uuid
from enum import Enum
from pydantic import BaseModel, Field, field_validator,UUID4
from sqlalchemy import JSON


class Status(str, Enum):
    NoSubmission = 'No Submission'
    NotCompleted = 'Not Completed'
    Pending = 'Pending'
    Approved = 'Approved'
    Declined = 'Declined'
    WithMinorIssues = 'Approved with minor issue'
    WithMajorIssues = 'Approved with major issue'

class AppraisalSubmissionBase(BaseModel):
    appraisals_id : UUID4
    staffs_id : UUID4
    appraisal_forms_id : UUID4
    submitted_values : Optional[Dict[str, Any]]
    started_at : Optional[date]
    completed_at : Optional[date]
    submitted : bool = False
    completed : bool = False
    approval_status : Status
    approval_date : Optional[date]
    comment : Optional[str]



     # Checking if fields are not empty and also not allowing the word string as value
    @field_validator('appraisals_id', 'staffs_id', 'appraisal_forms_id', mode='before')
    def check_non_empty_and_not_string(cls, v, info):
        if isinstance(v, str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty or the word "string"')
        return v


    # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('appraisals_id', 'staffs_id', 'appraisal_forms_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(str(v), version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v


    # Checking if submitted_at, approval_date and Completed_at is none, current time nad date will be submitted
    @field_validator('started_at', 'completed_at', 'approval_date', mode='before')
    def validate_and_convert_date_format(cls, v, info):
        if isinstance(v, date) is None:
            try:
                now = datetime.now()
                return now
            except ValueError:
                raise ValueError(f'\n{info.field_name} must be a valid date format and will be converted to YYYY-MM-DDTHH:MM:SS')
        return v
    

    @field_validator('submitted', 'completed', mode='before')
    def validate_boolean(cls, v, info) -> bool:
        if not isinstance(v, bool):
            raise ValueError(f'{info.field_name} must be a boolean value')
        return v


    # @field_validator('submitted_values')
    # def validate_competency_type(value: Dict[str, Any]) -> Dict[str, Any]:
    #      if not isinstance(value, dict) or not value:
    #         raise ValueError('Competency type must be a non-empty valid JSON object')
    #      return value
    

class AppraisalSubmissionCreate(AppraisalSubmissionBase):
    pass



class AppraisalSubmissionUpdate(AppraisalSubmissionBase):
    pass

class AppraisalSubmissionInDBBase(AppraisalSubmissionBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSubmissionSchema(AppraisalSubmissionInDBBase):
    pass