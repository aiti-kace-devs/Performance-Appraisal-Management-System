from datetime import date,time
from typing import Optional, Any, Dict

from pydantic import BaseModel
from pydantic import UUID4
from sqlalchemy import JSON


class Compentency_BankBase(BaseModel):
    appraisal_section_id = Optional[UUID4]
    staff_id = Optional[UUID4]
    compentency_type = JSON

class Compentency_BankCreate(Compentency_BankBase):
    appraisal_section_id = Optional[UUID4]
    staff_id = Optional[UUID4]
    compentency_type = JSON


class Compentency_BankUpdate(Compentency_BankBase):
    pass

class Compentency_BankInDBBase(Compentency_BankBase):
    id: UUID4

    class Config:
        orm_mode= True

class Compentency_BankSchema(Compentency_BankBase):
    pass