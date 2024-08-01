from typing import Any, Dict, Annotated, Optional, List
import uuid
from pydantic import BaseModel, Field, UUID4,field_validator
import json
from domains.appraisal.schemas.appraisal_cycle import AppraisalCycleSchema



class AppraisalConfigurationBase(BaseModel):
    appraisal_cycles_id: UUID4
    configuration: Dict[str, Any]
    


        
    # Custom Validator Functions
    @field_validator('appraisal_cycles_id', mode='before')
    def validate_appraisal_cycles_id(cls, value: UUID4) -> UUID4:
        try:
            uuid_obj = uuid.UUID(str(value), version=4)
            if uuid_obj.version != 4:
                raise ValueError("Not a Valid UUID4 data")
        except ValueError:
            raise ValueError('appraisal_cycles_id must be a valid UUID4')
        return value
    
    @field_validator('configuration', mode='before')
    def validate_configuration(cls, value: Any) -> Dict[str, Any]:
        if not value:
            raise ValueError('Configuration cannot be empty')
        

        if isinstance(value, dict):
            return value
        elif isinstance(value, str):
            try:
                json_obj = json.loads(value.replace("'", "\""))
                if not isinstance(json_obj, dict):
                    raise ValueError
                return json_obj
            except (json.JSONDecodeError, ValueError):
                raise ValueError('Configuration must be a valid JSON object or string')
        else:
            raise ValueError('Configuration must be a valid JSON object or string')
    class Config:
        arbitrary_types_allowed = True


   

class AppraisalConfigurationCreate(AppraisalConfigurationBase):

    pass

class AppraisalConfigurationUpdate(AppraisalConfigurationBase):
    pass

class AppraisalConfigurationInDBBase(AppraisalConfigurationBase):
    id: UUID4
   

    class Config:
        orm_mode = True
        

class AppraisalConfigurationSchema(AppraisalConfigurationInDBBase):
    pass


class AppraisalConfigurationWithCycleSchema(AppraisalConfigurationSchema):
    appraisal_cycle: Optional[AppraisalCycleSchema]

    class Config:
        orm_mode = True

class AppraisalCycleWithConfigurationsSchema(AppraisalCycleSchema):
    appraisal_configurations: List[AppraisalConfigurationSchema]

    class Config:
        orm_mode = True