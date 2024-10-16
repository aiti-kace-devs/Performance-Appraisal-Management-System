from datetime import date,time, datetime
from typing import Optional, Any, Dict, Annotated,List
from pydantic import BaseModel, Field, UUID4, constr, field_validator
from domains.appraisal.schemas.appraisal import GetAppraisalCycleBase,GetAppraisalSectionBase


class ReadAppraisalCycleBase(BaseModel):
    name: Annotated[str, Field(min_length=1)] = Field(...)
    description: Annotated[str, Field(min_length=1)] = Field(...)
    year: int = Field(default_factory=lambda: datetime.now().year)
    created_by: Optional[UUID4]



class AppraisalCycleBase(BaseModel):
    name: Annotated[str, Field(min_length=1)] = Field(...)
    description: Annotated[str, Field(min_length=1)] = Field(...)
    #year: int = Field(default_factory=lambda: datetime.now().year)

    @field_validator('name', 'description', mode='before')
    def validate_non_empty_and_no_string(cls, v, info):
        if not v.strip() or 'string' in v.strip():
            raise ValueError(f'{info.field_name} cannot be empty or contain the word "string"')
        return v

    # @field_validator('year')
    # def validate_year(cls, v):
    #     current_year = datetime.now().year
    #     if not (1000 <= v <= 9999):
    #         raise ValueError('Year must be in yyyy format')
    #     if v != current_year:
    #         raise ValueError('Year must be the current year')
    #     return v

class AppraisalCycleCreate(AppraisalCycleBase):
    pass

class AppraisalCycleUpdate(AppraisalCycleBase):
    pass

class AppraisalCycleInDBBase(ReadAppraisalCycleBase):
    id: UUID4

    class Config:
        orm_mode = True
        

class AppraisalCycleSchema(AppraisalCycleInDBBase):
    pass




class ReadAppraisalSectionWithCycleBase(BaseModel):
    id: UUID4
    name: Optional[str]
    description: Optional[str]
    year: Optional[int]
    created_by: Optional[UUID4]
    created_date: Optional[datetime]
    updated_date: Optional[datetime]
    appraisal_sections: Optional[List[GetAppraisalSectionBase]] = None