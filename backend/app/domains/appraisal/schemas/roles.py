from typing import Optional
from pydantic import BaseModel,field_validator



class RoleBase(BaseModel):
    name:str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    name:str
    description: Optional[str] = None
    
    @field_validator('name','description', mode='before')
    def check_non_empty_and_not_string(cls,v,info):
        if isinstance(v,str) and (v.strip() == '' or v.strip().lower() == 'string'):
            raise ValueError(f'\n{info.field_name} should not be empty "string"')
        
        #make minimum value 1
        if len(v.strip()) < 1:
            raise ValueError(f'{info.field_name} should have a minimum value of 1')

        return v
    
    


class RoleUpdate(RoleBase):
    pass

class RoleInDBBase(RoleBase):
    id: UUID4

    class Config:
        orm_mode= True

class RoleSchema(RoleBase):
    pass