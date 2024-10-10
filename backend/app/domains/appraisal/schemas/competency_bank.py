from datetime import date,time
from typing import Optional, Any, Dict,List
import uuid

from pydantic import BaseModel, field_validator
from pydantic import UUID4
from sqlalchemy import JSON



class ReadCompetencyBankBase(BaseModel):
    competency_type : Any



class CompetencyBankBase(BaseModel):
    competency_type : List[Any]


    # @staticmethod
    # def validate_competency_type(value: Dict[str, Any]) -> Dict[str, Any]:
    #      if not isinstance(value, dict) or not value:
    #         raise ValueError('Competency type must be a non-empty valid JSON object')
    #      return value

class CompetencyBankCreate(CompetencyBankBase):
    pass



class CompetencyBankUpdate(CompetencyBankBase):
    pass

class CompetencyBankInDBBase(ReadCompetencyBankBase):
    id: UUID4

    class Config:
        orm_mode= True

class CompetencyBankSchema(CompetencyBankInDBBase):
    pass