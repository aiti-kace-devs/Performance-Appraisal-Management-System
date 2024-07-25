from dateutil.parser import parse
from datetime import date, datetime,time
from typing import Annotated, Optional, Any, Dict
import uuid

from pydantic import BaseModel, Field, field_validator,UUID4
from sqlalchemy import JSON


class AppraisalSubmissionBase(BaseModel):
    appraisals_id : Optional[UUID4]
    staffs_id : Optional[UUID4]
    appraisal_forms_id : Optional[UUID4]
    submitted_values : Dict[str, str]
    started_at : Optional[date]
    completed_at : Optional[date]
    submitted : Optional[bool]
    completed : Optional[bool]
    approval_status : Optional[bool]
    approval_date : Optional[date]
    comment : Optional[str]

class AppraisalSubmissionCreate(AppraisalSubmissionBase):
    appraisals_id : Optional[UUID4]
    staffs_id : Optional[UUID4]
    appraisal_forms_id : Optional[UUID4]
    submitted_values : Dict[str, str]= Field(..., description="Values details")
    started_at : Optional[date]
    completed_at : Optional[date]
    approval_date : Optional[date]
    submitted : Optional[bool]
    completed : Optional[bool]
    approval_status : Optional[bool]
    comment : Optional[str] = Field(..., min_length=1)



 # Checking if fields are not empty and also not allowing the word string as value
    @field_validator('appraisals_id', 'staffs_id', 'appraisal_forms_id', 'comment', mode='before')
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


    # Checking if started_at, approval_date and Completed_at is none, current time nad date will be submitted
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
    


    @field_validator('submitted_values')
    @classmethod
    def validate(cls, values):
        # Perform additional custom validation if necessary
        details = values.get("details", {})
        for key, value in details.items():
            if not key.isalpha():  # Ensure keys are alphabetic
                raise ValueError(f"Key '{key}' is not alphabetic")
        return values
    
    @field_validator('submitted_values')
    def metadata_must_not_be_empty(cls, values):
        for key, value in values.items():
            if not key.strip():
                raise ValueError('details keys must not be empty')
            if not value.strip():
                raise ValueError('details values must not be empty')
        return values

    
    @field_validator('submitted_values')
    def entry_not_be_string(cls, values):
        for key, value in values.items():
            if value == "string":
                raise ValueError(f'entry {key}: "string" is not allowed')
        return values


class AppraisalSubmissionUpdate(AppraisalSubmissionBase):
    pass

class AppraisalSubmissionInDBBase(AppraisalSubmissionBase):
    id: UUID4

    class Config:
        orm_mode= True

class AppraisalSubmissionSchema(AppraisalSubmissionBase):
    pass