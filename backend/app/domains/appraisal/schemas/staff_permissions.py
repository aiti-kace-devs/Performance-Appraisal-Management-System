from datetime import date,time
from typing import Optional, Any, Dict, List
from pydantic import BaseModel,UUID4, field_validator, model_validator
import uuid

class StaffPermissionBase(BaseModel):
    staffs_id : UUID4
    roles_id : UUID4
    permissions_id : UUID4

class StaffPermissionCreate(StaffPermissionBase):
    pass

    # Checking if fields are not empty and also not allowing the word string as value
    @field_validator('staffs_id', 'roles_id', 'permissions_id', mode='before')
    def check_non_empty_and_not_string(cls, v, info):
        if isinstance(v, str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty or the word "string"')
        return v

    # Checking if UUID4 fields accept only UUID4 as value
    @field_validator('staffs_id', 'roles_id', 'permissions_id', mode='before')
    def validate_fields_with_uuid4(cls, v, info):
        try:
            uuid.UUID(str(v), version=4)
        except ValueError:
            raise ValueError(f'\n{info.field_name} must have a valid UUID4')
        return v

class StaffPermissionUpdate(StaffPermissionBase):
    pass

class StaffPermissionInDBBase(StaffPermissionBase):
    id: UUID4

    class Config:
        orm_mode= True

class StaffPermissionSchema(StaffPermissionInDBBase):
    pass

class PermissionOut(BaseModel):
    id: UUID4
    name: str

class StaffPermissionsOut(BaseModel):
    staff_id: UUID4
    staff_name: str
    permissions: List[PermissionOut]

class StaffUpdatePermissions(BaseModel):
    permissions_ids: List[UUID4]  # List of permission IDs to assign to the staff

    class Config:
        orm_mode = True