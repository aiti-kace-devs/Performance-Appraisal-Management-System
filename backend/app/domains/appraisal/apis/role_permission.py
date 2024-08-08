from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session


from domains.appraisal.schemas import role_permissions as schema
from domains.appraisal.services.role_permission import role_perm_service  as actions 


from db.session import get_db

# APIRouter creates path operations for assigning roles and permission
role_perm_router = APIRouter(
    prefix="/roles-permission",
    tags=["Roles-Permission"],
    responses={404: {"description": "Not found"}},
)


@role_perm_router.post("/", response_model=schema.RoleWithPermissions)
def create_new_role_permission(*, payload: schema.RolePermissionCreate, db:Session=Depends(get_db)):
    new_role_perm = actions.create_role_perm(role_perm=payload, db=db)
    return new_role_perm

## returns a role and it associate permissions
@role_perm_router.get("/{role_id}", response_model=schema.RolePermissionRead)
def get_permissions_by_role_id(role_id: UUID4, db: Session = Depends(get_db)):
    try:
        role_permissions = actions.get_permissions_by_role_id(db=db, role_id=role_id)
        return role_permissions
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

## endpoint to 
@role_perm_router.get("/", response_model=List[schema.RolePermissionRead])
def get_all_roles_perms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    all_roles_perms = actions.get_all_roles_perms(db=db, skip=skip, limit=limit)
    return all_roles_perms

## endpoint to update the 
@role_perm_router.put("/{role_id}")
async def update_roles_perm(role_id: UUID4, db: Session = Depends(get_db)):
    update_role_perm = actions.update_role_perm(role_id=role_id, db=db)
    return update_role_perm

