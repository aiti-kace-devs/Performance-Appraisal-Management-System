from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from sqlalchemy import func 

from db.base_class import UUID
from domains.appraisal.respository.role_permission import role_perm_actions as role_perm_repo
from domains.appraisal.schemas.role_permissions import RolePermissionCreate, RolePermissionUpdate, RolePermissionRead, PermissionRead
from domains.appraisal.models.staff_role_permissions import Role, Permission, role_permissions
# from domains.appraisal.models.roles import Role 
# from domains.appraisal.models.permissions import Permission


class RolePermssionService:

    def get_permissions_by_role_id(self, db: Session, role_id: UUID) -> RolePermissionRead:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role does not exist"
            )
        permissions = [
            PermissionRead(id=perm.id, name=perm.name)
            for perm in role.permissions
        ]
        return RolePermissionRead(id=role.id, name=role.name, permissions=permissions)


    def get_all_roles_perms(self, db: Session, skip: int=0, limit: int=10):

        # return role_repo.get_all(db=db, skip=skip, limit=limit)
        roles = db.query(Role).offset(skip).limit(limit).all()
        return [self._convert_role_to_read(role) for role in roles]


    
    def create_role_perm(self, *, role_perm: RolePermissionCreate, db: Session) -> RolePermissionRead:
        # Check if the role name already exists
        existing_role = db.query(Role).filter(Role.name == role_perm.name).first()
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role '{role_perm.name}' already exists."
            )

        db_role = Role(name=role_perm.name)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)

        for per in role_perm.permissions:
            db_permission = db.query(Permission).filter(Permission.name == per.name).first()
            if not db_permission:
                db_permission = Permission(name=per.name)
                db.add(db_permission)
                db.commit()
                db.refresh(db_permission)

            db_role.permissions.append(db_permission)

        db.commit()
        db.refresh(db_role)
        
        return self._convert_role_to_read(db_role) 
    
    def remove_permission_from_role(self, db: Session, role_id: UUID, permission_name: str):
        role = db.query(Role).filter(
            Role.id == role_id,
        ).first()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Role not found"
            )
        
        permission = db.query(Permission).filter(
            Permission.name == permission_name, 
        ).first()

        if not permission:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND, 
                detail = "Permission not found"
            )
        
        if permission in role.permissions:
            role.permissions.remove(permission)
            db.commit()
        
        return role
        
    def update_role_perms(self, db: Session, role_id: UUID, new_permissions: List[str]) -> RolePermissionRead:
        # Fetch the role from the database 
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                details=f"Role with id {role_id} found"
            )

        # Clear existing permissions for the role 
        role.permissions.clear() 

        # Retrieve the new permissions by their IDs 
        permissions = db.query(Permission).filter(Permission.name.in_(new_permissions)).all()

        if not permissions: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Some permissions not found"
            )

        ## Assign new permissions to the role 
        role.permissions.extend(permissions)
 
        return {
            "role_id": role_id,
            "updated_permissions": [perm.name for perm in role.permissions]
        }
    #     return self._convert_role_to_read(role)
    #     # return role
    
    # def _convert_role_to_read(self, role: Role) -> RolePermissionRead:
    #     permissions = [
    #         PermissionRead(id=perm.id, name=perm.name)
    #         for perm in role.permissions
    #     ]
    #     return RolePermissionRead(id=role.id, name=role.name, permissions=permissions)

role_perm_service = RolePermssionService()