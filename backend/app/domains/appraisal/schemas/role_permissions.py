
from pydantic import BaseModel, Field, validator


class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int

    @validator('role_id', 'permission_id')
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