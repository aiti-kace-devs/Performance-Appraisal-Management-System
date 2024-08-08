from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.role import role_actions as role_repo 
from domains.appraisal.schemas.roles import RoleCreate, RoleUpdate, RoleRead

from domains.appraisal.models.role_permissions import Permission


class PermissionService:
    def get_perm_by_id(self, db: Session, perm_id: UUID) -> RoleRead:
        # role = role_repo.get(db=db, id=role_id)
        perm = db.query(Permission).filter(Permission.id == perm_id).first()
        if not perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="role does not exits"
            )
        return perm
    
    def get_all_perms(self, db: Session, skip: int=0, limit: int=10):
        
        # return role_repo.get_all(db=db, skip=skip, limit=limit)
        return db.query(Permission).offset(skip).limit(limit).all()
    
perm_service = PermissionService()