
from pydantic import BaseModel, field_validator
import uuid

class RolePermissionBase(BaseModel):
    role_id: uuid
    permission_id: uuid

    @field_validator('role_id', 'permission_id')
    def id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("ID must be a positive integer")
        return value

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionUpdate(RolePermissionBase):
    pass

class RolePermission(RolePermissionBase):
    id: int

    class Config:
        orm_mode = True