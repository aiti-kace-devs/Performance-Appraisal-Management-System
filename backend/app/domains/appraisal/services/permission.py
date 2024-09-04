from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.role import role_actions as role_repo 
from domains.appraisal.schemas.roles import RoleCreate, RoleUpdate, RoleRead
from domains.appraisal.schemas.permissions import PermissionUpdate

from domains.appraisal.models.role_permissions import Permission, Role


class PermissionService:

    def add_permission_to_role(self, db: Session, role_id: UUID, permission_name: str):
        role = db.query(Role).filter(Role.id == role_id)
        if not role:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, 
                detail="Role not found"
            )
        permission = db.query(Permission).filter(Permission.name == permission_name).first()

        ## if the permission does not exist, create it
        if not permission:
            permission = Permission(name=permission_name)
            db.add(permission)
            db.commit()
            db.refresh(permission)

        if permission not in role.permissions:
            ## Add the permission to the role only if it's not already present
            role.permssions.append(permission)
            db.commit()
            db.refresh(role)

            return role

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
    
    def update_permission(self, db: Session, permission_id: UUID, permission_update: PermissionUpdate):
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, 
                detail="Permission not found"
            )

        permission.name = permission_update.name 
        db.commit()
        db.refresh(permission)
        return permission
    
perm_service = PermissionService()