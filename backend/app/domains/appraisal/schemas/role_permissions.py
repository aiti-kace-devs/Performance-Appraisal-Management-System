from typing import List, Optional, Union,Annotated
from pydantic import BaseModel, Field, field_validator, UUID4 
# from domains.appraisal.schemas.permissions import PermissionCreate, PermissionRead

class PermissionCreate(BaseModel):
    name: str

class RolePermissionCreate(BaseModel):
    name: str
    permissions: List[PermissionCreate]

class PermissionBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class PermissionRead(PermissionBase):
    id: UUID4




class RolePermissionBase(BaseModel):
    name: str = Field(min_length=1, max_length=50, example="admin")
    permissions: List[PermissionCreate] = []

    # @field_validator('name')
    # def name_must_not_be_empty(cls, value):
    #     if not value or value.isspace() or (value.lower() == 'string'):
    #         raise ValueError("Role name must not be empty or only whitespace or string")
    #     return value
    
    # role_id: UUID4 
    # permission_id: UUID4 

    # @field_validator('role_id', 'permission_id')
    # def id_must_be_positive(cls, value):
    #     if value <= 0:
    #         raise ValueError("ID must be a positive integer")
    #     return value

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionUpdate(RolePermissionBase):
    pass

class RolePermission(RolePermissionBase):
    id: UUID4 

    class Config:
        orm_mode = True

class RolePermissionRead(BaseModel):
    id: UUID4
    name: str
    permissions: List[PermissionRead]

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Permission(PermissionBase):
    id: UUID4

class RoleWithPermissions(RoleBase):
    id: UUID4
    permissions: List[Permission]

    class Config:
        orm_mode = True