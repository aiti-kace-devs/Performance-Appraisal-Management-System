from datetime import date,time
from typing import Optional, Any, Dict
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic import UUID4


class KraBankBase(BaseModel):
    focus_area: Dict[str, Any] = Field(..., description="Focus area as a JSON object")
    created_date: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC), description="Created Date")

class KraBankBaseCreate(KraBankBase):
    focus_area: Dict[str, Any] = Field(..., description="Focus area as a JSON object")
    created_date: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC), description="Created Date")

class KraBankUpdate(KraBankBase):
    pass

class KraBankInDBBase(KraBankBase):
    id: UUID4

    class Config:
        orm_mode= True

class KraBankSchema(KraBankBase):
    pass