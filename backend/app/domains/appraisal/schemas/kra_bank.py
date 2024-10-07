from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel, Field, field_validator, root_validator


class KraBankBase(BaseModel):
    department_id: Optional[UUID4] = Field(..., description="Department ID")
    focus_area: List[Dict[str, Any]] = Field(..., description="Focus Area")


class KraBankCreate(KraBankBase):
    department_id: Optional[UUID4] = Field(..., description="Department ID")
    focus_area: List[Dict[str, Any]] = Field(..., description="Focus Area")
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @root_validator(pre=True)
    def check_non_empty_fields(cls, values):
        for field_name, value in values.items():
            if isinstance(value, str) and value == "string":
                raise ValueError(f"Field {field_name} cannot be 'string'")
            if value is None or (isinstance(value, str) and value.strip() == ""):
                raise ValueError(f"Field {field_name} cannot be empty")
        return values

    @field_validator("focus_area")
    def validate_focus_area(cls, v):
        if not isinstance(v, list):
            raise ValueError("focus_area must be a list of dictionaries")
        for item in v:
            if not isinstance(item, dict):
                raise ValueError("Each item in focus_area must be a dictionary")
        return v



class KraBankUpdate(KraBankBase):
    pass


class KraBankInDBBase(KraBankBase):
    id: UUID4

    class Config:
        orm_mode = True


class KraBankSchema(KraBankInDBBase):
    pass
