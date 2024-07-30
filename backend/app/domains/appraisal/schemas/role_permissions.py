
from pydantic import BaseModel, field_validator, UUID4 


class RolePermissionBase(BaseModel):
    role_id: UUID4 
    permission_id: UUID4 

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
    id: UUID4 

    class Config:
        orm_mode = True

class RolePermissionRead(RolePermissionBase):
    pass