from typing import List, Any
import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.base_class import UUID
from domains.appraisal.respository.staff_permissions import staff_permission_action as staff_permission_repo
from domains.appraisal.schemas.staff_permissions import StaffPermissionSchema, StaffPermissionUpdate, StaffPermissionCreate


class StaffPermissionService:

    def create_staff_permissions(self, *, db: Session, staff_permission:StaffPermissionCreate) -> StaffPermissionSchema:
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
