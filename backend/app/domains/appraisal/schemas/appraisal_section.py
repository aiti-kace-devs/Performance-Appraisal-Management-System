from typing import Any, Dict, Annotated, Optional,List
import uuid
from pydantic import BaseModel, Field, UUID4, ValidationError, field_validator
from sqlalchemy.orm import Session
from domains.appraisal.models.appraisal_cycle import AppraisalCycle  # Import the actual SQLAlchemy model
from domains.appraisal.models.appraisal_section import AppraisalSection 


# Custom Validator Function


class AppraisalCycleBase(BaseModel):
    id: Optional[UUID4] = None
    name: Optional[str] = None


class ReadAppraisalSectionBase(BaseModel):
    name: Annotated[str, Field(min_length=1)] = Field(...)
    description: Annotated[str, Field(min_length=1)] = Field(...)
    appraisal_year: Optional[int]
    appraisal_cycle: Optional[AppraisalCycleBase] = None
    created_by: Optional[UUID4] 



class AppraisalSectionBase(BaseModel):
    name: Annotated[str, Field(min_length=1)] = Field(...)
    description: Annotated[str, Field(min_length=1)] = Field(...)
    appraisal_cycle_id: UUID4 


    @field_validator('name', 'description', mode='before')
    def validate_non_empty_and_no_string(cls, v, info):
        if not v or 'string' in v:
            raise ValueError(f'{info.field_name} cannot be empty or contain the word "string"')
        return v
    



class AppraisalSectionCreate(AppraisalSectionBase):
    pass

class AppraisalSectionUpdate(AppraisalSectionBase):
    pass

class AppraisalSectionInDBBase(ReadAppraisalSectionBase):
    id: UUID4

    class Config:
        orm_mode = True

class AppraisalSectionSchema(AppraisalSectionInDBBase):
    pass
