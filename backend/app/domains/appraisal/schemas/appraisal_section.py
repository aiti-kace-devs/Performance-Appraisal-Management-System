from typing import Any, Dict, Annotated
import uuid
from pydantic import BaseModel, Field, UUID4, ValidationError, field_validator
from sqlalchemy.orm import Session
from domains.appraisal.models.appraisal_cycle import AppraisalCycle  # Import the actual SQLAlchemy model
from domains.appraisal.models.appraisal_section import AppraisalSection 

# Custom Validator Function
def validate_appraisal_cycles_id(value: UUID4, session: Session) -> UUID4:
    # Ensure the ID is in UUID4 format
    try:
        uuid.UUID(str(value), version=4)
    except ValueError:
        raise ValueError('appraisal_cycles_id must be a valid UUID4')
    
    # Check if the UUID exists in the appraisal_cycle table
    if not session.query(AppraisalCycle).filter(AppraisalCycle.id == value).first():
        raise ValueError('appraisal_cycles_id must reference an existing row in the appraisal_cycle table')
    
    if session.query(AppraisalSection).filter(AppraisalSection.appraisal_cycles_id == value).first():
        raise ValueError('appraisal_cycles_id already exist in table \'appraisal_sections\' ' )

    return value

class AppraisalSectionBase(BaseModel):
    appraisal_cycles_id: Annotated[UUID4, Field(...)]
    name: Annotated[str, Field(min_length=1)] = Field(...)
    description: Annotated[str, Field(min_length=1)] = Field(...)


    @field_validator('name', 'description', mode='before')
    def validate_non_empty_and_no_string(cls, v, info):
        if not v or 'string' in v:
            raise ValueError(f'{info.field_name} cannot be empty or contain the word "string"')
        return v
    

    @staticmethod
    def validate_appraisal_cycles_id_with_session(value: UUID4, session: Session) -> UUID4:
        return validate_appraisal_cycles_id(value, session)

    

    def validate(self, session: Session) -> 'AppraisalSectionBase':
        self.appraisal_cycles_id = self.validate_appraisal_cycles_id_with_session(self.appraisal_cycles_id, session)
    
        return self

class AppraisalSectionCreate(AppraisalSectionBase):
    pass

class AppraisalSectionUpdate(AppraisalSectionBase):
    pass

class AppraisalSectionInDBBase(AppraisalSectionBase):
    id: UUID4

    class Config:
        orm_mode = True

class AppraisalSectionSchema(AppraisalSectionBase):
    pass
