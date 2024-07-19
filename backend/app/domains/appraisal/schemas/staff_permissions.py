from datetime import date,time
from typing import Optional, Any, Dict
from pydantic import BaseModel,UUID4



class StaffPermissionBase(BaseModel):
    staffs_id : UUID4
    roles_id : UUID4
    permissions_id : UUID4

class StaffPermissionCreate(BaseModel):
    staffs_id : UUID4
    roles_id : UUID4
    permissions_id : UUID4

class StaffPermissionUpdate(StaffPermissionBase):
    pass

class StaffPermissionInDBBase(StaffPermissionBase):
    id: UUID4

    class Config:
        orm_mode= True

class StaffPermissionSchema(StaffPermissionBase):
    pass