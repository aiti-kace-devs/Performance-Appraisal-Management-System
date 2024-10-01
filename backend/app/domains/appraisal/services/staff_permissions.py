from typing import List, Any
import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.base_class import UUID
from domains.appraisal.respository.staff_permissions import staff_permission_action as staff_permission_repo
from domains.appraisal.schemas.staff_permissions import StaffPermissionSchema, StaffPermissionUpdate, StaffPermissionCreate
from domains.appraisal.models.staff_role_permissions import Staff, staff_permissions, Role, Permission
# from domains.appraisal.models.staff_permissions import StaffPermission
# from domains.appraisal.models.staff_role_permissions import Role, Permission
# from domains.appraisal.models.role_permissions import Permission

class StaffPermissionService:

    def create_staff_permissions(self, *, db: Session, staff_permission:StaffPermissionCreate) -> StaffPermissionSchema:
        # checking if Staff_id exist in Staff table
        check_staff_id = db.query(Staff).filter(Staff.id == staff_permission.staffs_id).first()
        if not check_staff_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="staff with id %s not found in staff table" % staff_permission.staffs_id)
        
        # Check for duplicate staff IDs in the staff permission table.
        check_staff_id = db.query(staff_permissions).filter(staff_permissions.staffs_id == staff_permission.staffs_id).first()
        if check_staff_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="staff with id %s already exist in staff_permission table" % staff_permission.staffs_id)
        
        # Checking if the roles ID exists on the roles table
        check_roles_id = db.query(Role).filter(Role.id == staff_permission.roles_id).first()
        if not check_roles_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="role with id %s not found in roles table" % staff_permission.roles_id)

        # Check if the permissions ID exists on the permissions table
        check_permission_id = db.query(Permission).filter(Permission.id == staff_permission.permissions_id).first()
        if not check_permission_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission with id %s not found in permissions table" % staff_permission.permissions_id)

        staff_permissions_obj = staff_permission_repo.create(db=db, obj_in = staff_permission)
        return staff_permissions_obj
    

    def get_staff_permissions(self, *, db: Session, id: UUID) -> StaffPermissionSchema:
        staff_permissions_obj = staff_permission_repo.get(db=db, id=id)
        if not staff_permissions_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff_permission not found")
        return staff_permissions_obj

    def get_all_staff_permissions(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffPermissionSchema]:
        staff_permission_obj = staff_permission_repo.get_all(db=db, skip=skip, limit=limit)
        return staff_permission_obj
    
    def update_staff_permissions(self, *, db: Session, id: UUID,  staff_permission: StaffPermissionUpdate) -> StaffPermissionSchema:
        staff_permissions_obj = staff_permission_repo.get(db=db, id=id)
        if not staff_permissions_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff_permission_id not found")
        staff_permissions_obj = staff_permission_repo.update(db=db, db_obj=staff_permissions_obj, obj_in=staff_permission)
        return staff_permissions_obj

    def delete_staff_permissions(self, *, db: Session, id: UUID) -> StaffPermissionSchema:
        staff_permissions_obj = staff_permission_repo.get(db=db, id=id)
        if not staff_permissions_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff_permissions_id not found")
        staff_permissions_obj = staff_permission_repo.remove(db=db, id=id)
        return staff_permissions_obj

staff_permission_service = StaffPermissionService()
