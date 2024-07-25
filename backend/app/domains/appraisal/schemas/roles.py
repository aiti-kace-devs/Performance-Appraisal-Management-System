from typing import Optional
from pydantic import BaseModel,field_validator

from typing import List, Optional, Union,Annotated
from pydantic import BaseModel, Field, field_validator, UUID4
from schemas.permissions import PermissionCreate, Permission



class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=50, example="admin")

    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value or value.isspace() or (value.lower() == 'string'):
            raise ValueError("Role name must not be empty or only whitespace or string")
        return value

class RoleCreate(RoleBase):
    permissions: List[PermissionCreate] = []

    @field_validator('permissions', pre=True, each_item=True)
    def permissions_must_be_valid(cls, value):
        if not isinstance(value, PermissionCreate):
            raise ValueError("Invalid permission data")
        return value

class RoleUpdate(RoleBase):
    permissions: List[PermissionCreate] = []

    @field_validator('permissions', pre=True, each_item=True)
    def permissions_must_be_valid(cls, value):
        if not isinstance(value, PermissionCreate):
            raise ValueError("Invalid permission data")
        return value

class ReadRole(RoleBase):
    id: UUID4
    permissions: List[Permission] = []

    class Config:
        orm_mode = True
