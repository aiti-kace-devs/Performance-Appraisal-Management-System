from typing import List, Any
import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.base_class import UUID
from pydantic import UUID4
from domains.appraisal.respository.staff_permissions import staff_permission_action as staff_permission_repo
from domains.appraisal.schemas.staff_permissions import StaffPermissionSchema, StaffPermissionUpdate, StaffPermissionCreate
from domains.appraisal.models.staff_role_permissions import Staff, staff_permissions, Role, Permission
from domains.auth.models.users import User
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
    

    # def get_staff_permissions(self, *, db: Session, id: UUID) -> StaffPermissionSchema:
    #     staff_permissions_obj = staff_permission_repo.get(db=db, id=id)
    #     if not staff_permissions_obj:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff_permission not found")
    #     return staff_permissions_obj

    def get_all_staff_permissions(self, *, db: Session, skip: int = 0, limit: int = 100):
        # Query to get all staff permissions
        staff_permissions_data = db.query(Staff, Permission).join(staff_permissions, Staff.id == staff_permissions.c.staff_id).join(Permission, staff_permissions.c.permission_id == Permission.id).all()
        
        result = {}
        for staff, permission in staff_permissions_data:
            # If staff already in result, append the permission to the list
            if staff.id in result:
                result[staff.id]['permissions'].append({
                    "id": permission.id,
                    "name": permission.name
                })
            else:
                # If staff not in result, initialize with permissions as a list
                result[staff.id] = {
                    "staff_id": staff.id,
                    "staff_name": f"{staff.first_name} {staff.last_name}",
                    "permissions": [{
                        "id": permission.id,
                        "name": permission.name
                    }]
                }

        # Return the result as a list of staff with their permissions
        return list(result.values())

    def get_staff_permissions_by_staff_id(self, * , db: Session, staff_id: UUID):
        # Check if staff exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        
        # Query to get permissions for a specific staff
        permissions_data = db.query(Permission).join(staff_permissions, Permission.id == staff_permissions.c.permission_id).filter(staff_permissions.c.staff_id == staff_id).all()

        get_user_from_staff = db.query(User).filter(User.staff_id == staff_id).first()
        get_staff_role = db.query(Role).filter(Role.id == get_user_from_staff.role_id).first()

        result = {
            "staff_id": staff.id,
            "staff_name": f"{staff.first_name} {staff.last_name} {staff.other_name}",
            "role": {
                "id": get_staff_role.id,
                "name": get_staff_role.name,
            },
            "permissions": [{"id": permission.id, "name": permission.name} for permission in permissions_data]
        }

        return result

    def update_staff_permissions(self, db: Session, staff_id: UUID, new_permissions_ids: List[UUID]):
        # Check if staff exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

        # Remove existing permissions for the staff
        db.execute(staff_permissions.delete().where(staff_permissions.c.staff_id == staff_id))

        # Add new permissions
        for permission_id in new_permissions_ids:
            # Check if the permission exists
            permission = db.query(Permission).filter(Permission.id == permission_id).first()
            if not permission:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permission with ID {permission_id} not found")

            # Insert the new staff-permission association
            staff_permission = {
                "staff_id": staff.id,
                "permission_id": permission_id
            }
            db.execute(staff_permissions.insert().values(staff_permission))

        db.commit()  # Commit the changes

            # Return updated permissions
        updated_permissions = db.query(Permission).join(
            staff_permissions, Permission.id == staff_permissions.c.permission_id
        ).filter(staff_permissions.c.staff_id == staff_id).all()

        return {
            "staff_id": staff_id,
            "permissions": [{"id": permission.id, "name": permission.name} for permission in updated_permissions]
        }
    # def update_staff_permissions(self, *, db: Session, staff_id: UUID,  new_permissions_ids: List[UUID]):
    #     # Check if staff exists
    #     staff = db.query(Staff).filter(Staff.id == staff_id).first()
    #     if not staff:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    #     # Remove existing permissions for the staff
    #     db.execute(staff_permissions.delete().where(staff_permissions.c.staff_id == staff_id))

    #     # Assign new permissions
    #     for permission_id in permission_ids:
    #         permission = db.query(Permission).filter(Permission.id == permission_id).first()
    #         if not permission:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Permission with ID {permission_id} not found")

    #         db.execute(
    #             staff_permissions.insert().values(staff_id=staff_id, permission_id=permission_id)
    #         )

    #     db.commit()

    #     # Return the updated permissions
    #     updated_permissions = db.query(Permission).join(
    #         staff_permissions, Permission.id == staff_permissions.c.permission_id
    #     ).filter(staff_permissions.c.staff_id == staff_id).all()

        # return [{"id": permission.id, "name": permission.name} for permission in updated_permissions]


    # def delete_staff_permissions(self, *, db: Session, id: UUID) -> StaffPermissionSchema:
    #     staff_permissions_obj = staff_permission_repo.get(db=db, id=id)
    #     if not staff_permissions_obj:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff_permissions_id not found")
    #     staff_permissions_obj = staff_permission_repo.remove(db=db, id=id)
    #     return staff_permissions_obj

staff_permission_service = StaffPermissionService()
