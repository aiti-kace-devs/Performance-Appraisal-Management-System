from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


from db.base_class import UUID
from domains.appraisal.respository.role import role_actions as role_repo 
from domains.appraisal.schemas.roles import RoleCreate, RoleUpdate, RoleRead



class RoleService:
    def get_role_by_id(self, db: Session, role_id: UUID) -> RoleRead:
        role = role_repo.get(db=db, id=role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="role does not exits"
            )
        return role
    
    def get_all_roles(self, db: Session, skip: int=0, limit: int=10) -> List[RoleRead]:
        return role_repo.get_all(db=db, skip=skip, limit=limit)
    
    
role_service = RoleService()