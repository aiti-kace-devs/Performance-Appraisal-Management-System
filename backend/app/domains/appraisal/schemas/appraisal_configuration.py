from typing import Any, Dict, Annotated
import uuid
from pydantic import BaseModel, Field, UUID4, ValidationError
from sqlalchemy.orm import Session
from domains.appraisal.models.appraisal_cycle import AppraisalCycle  # Import the actual SQLAlchemy model
from domains.appraisal.models.appraisal_configuration import AppraisalConfiguration 

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
    
    if session.query(AppraisalConfiguration).filter(AppraisalConfiguration.appraisal_cycles_id == value).first():
        raise ValueError('appraisal_cycles_id already exist in table \'appraisal_configurations\' ' )

    return value

class AppraisalConfigurationBase(BaseModel):
    appraisal_cycles_id: Annotated[UUID4, Field(...)]
    configuration: Annotated[Dict[str, Any], Field(...)]

    @staticmethod
    def validate_appraisal_cycles_id_with_session(value: UUID4, session: Session) -> UUID4:
        return validate_appraisal_cycles_id(value, session)

    @staticmethod
    def validate_configuration(value: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(value, dict) or not value:
            raise ValueError('Configuration must be a non-empty valid JSON object')
        return value
    
    

    def validate(self, session: Session) -> 'AppraisalConfigurationBase':
        self.appraisal_cycles_id = self.validate_appraisal_cycles_id_with_session(self.appraisal_cycles_id, session)
        self.configuration = self.validate_configuration(self.configuration)
        return self

class AppraisalConfigurationCreate(AppraisalConfigurationBase):
    pass

class AppraisalConfigurationUpdate(AppraisalConfigurationBase):
    pass

class AppraisalConfigurationInDBBase(AppraisalConfigurationBase):
    id: UUID4

    class Config:
        orm_mode = True

class AppraisalConfigurationSchema(AppraisalConfigurationBase):
    pass
