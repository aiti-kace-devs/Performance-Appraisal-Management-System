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
        role = db.query(Role).filter(Role.id == role_id).first()
        
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
            role.permissions.append(permission)
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
    
    # def update_permission(self, db: Session, permission_id: UUID, permission_update: PermissionUpdate):
    #     permission = db.query(Permission).filter(Permission.id == permission_id).first()
    #     if not permission:
    #         raise HTTPException(
    #             status_code = status.HTTP_404_NOT_FOUND, 
    #             detail="Permission not found"
    #         )

    #     permission.name = permission_update.name 
    #     db.commit()
    #     db.refresh(permission)
    #     return permission

    def update_permission(db: Session, permissions: List[PermissionUpdate]):
        """
        Update multiple permissions in the database 

        : param db: Database session
        : param permissions: A list of permissions to update
        """
        for perm_update in permissions:
            ## Query for the permission by its ID
            permission = db.query(Permission).filter(Permission.id == perm_update.id).first()

            ## if the permission doesn't exist, raise an exception 
            if not permission:
                raise HTTPException(status_code=404, detail=f"Permission with ID{perm_update.id} not found")

            if perm_update.name: 
                ## Check if a permission with the new name already exists to avoid duplicate 
                existing_perm = db.query(Permission).filter(Permission.name == perm_update.name).first()

                if existing_perm and existing_perm.id != perm_update.id:
                    raise HTTPException(status_code400, details=f"Permission name '{perm_update.name} already exits")

                #Update the permission name
                permission.name = perm_update.name 

        db.commit()
        return {"details": "Permission updated successfully"}
    
perm_service = PermissionService()