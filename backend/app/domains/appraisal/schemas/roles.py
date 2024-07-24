from typing import List, Optional, Union,Annotated
from pydantic import BaseModel, Field, validator
from schemas.permissions import PermissionCreate, Permission


class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=50, example="admin")

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value or value.isspace():
            raise ValueError("Role name must not be empty or only whitespace")
        return value

class RoleCreate(RoleBase):
    permissions: List[PermissionCreate] = []

    @validator('permissions', pre=True, each_item=True)
    def permissions_must_be_valid(cls, value):
        if not isinstance(value, PermissionCreate):
            raise ValueError("Invalid permission data")
        return value

class RoleUpdate(RoleBase):
    permissions: List[PermissionCreate] = []

    @validator('permissions', pre=True, each_item=True)
    def permissions_must_be_valid(cls, value):
        if not isinstance(value, PermissionCreate):
            raise ValueError("Invalid permission data")
        return value

class Role(RoleBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        orm_mode = True

# class RoleBase(BaseModel):
#     name:str
#     description: Optional[str] = None


# class RoleCreate(RoleBase):
#     name:str
#     description: Optional[str] = None
    
#     @field_validator('name','description', mode='before')
#     def check_non_empty_and_not_string(cls,v,info):
#         if isinstance(v,str) and (v.strip() == '' or v.strip().lower() == 'string'):
#             raise ValueError(f'\n{info.field_name} should not be empty "string"')
        
#         #make minimum value 1
#         if len(v.strip()) < 1:
#             raise ValueError(f'{info.field_name} should have a minimum value of 1')

#         return v
    
    


# class RoleUpdate(RoleBase):
#     pass

# class RoleInDBBase(RoleBase):
#     id: UUID4

#     class Config:
#         orm_mode= True

# class RoleSchema(RoleBase):
#     pass