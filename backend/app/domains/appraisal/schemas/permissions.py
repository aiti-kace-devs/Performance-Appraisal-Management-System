from pydantic import BaseModel, Field, field_validator
import uuid

class PermissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, example="read:data")

    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value or value.isspace() or (value.lower() == "string"):
            raise ValueError("Permission name must not be empty or only whitespace")
        return value

class PermissionCreate(PermissionBase):
    pass 

class Permission(PermissionBase):
    id: uuid

    class Config:
        orm_mode = True 
        