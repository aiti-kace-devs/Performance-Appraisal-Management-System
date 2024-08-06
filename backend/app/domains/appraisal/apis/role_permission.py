# from typing import Any, List
# from fastapi import APIRouter, Depends
# from fastapi import HTTPException
# from pydantic import UUID4
# from sqlalchemy.orm import Session
# from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

# from domains.appraisal.schemas import role_permissions as schema
# from domains.appraisal.services.role_permission import role_perm_service  as actions 

# # from domains.appraisal.schemas import roles as schema
# # from domains.appraisal.services.role import role_service as actions 


# from db.session import get_db

# # APIRouter creates path operations for assigning roles and permission
# role_perm_router = APIRouter(
#     prefix="/roles-permission",
#     tags=["Roles-Permission"],
#     responses={404: {"description": "Not found"}},
# )


# # @role_perm_router.post("/assign-role-perm/", response_model=schema.RolePermissionRead)
# # def create_new_role_permission(*, payload: schema.RolePermissionCreate, db:Session=Depends(get_db)):
# #     new_role_perm = actions.create_role_perm(payload, db)
# #     return new_role_perm

# ## returns a role and it associate permissions
# @role_perm_router.get("/{role_id}", response_model=schema.RolePermissionRead)
# def get_row_perm(role_id: UUID4, db: Session = Depends(get_db)):
#     role = actions.get_role_perm(role_id=role_id, db=db)
#     return role 

# ## endpoint to 
# @role_perm_router.get("/", response_model=List[schema.RolePermissionRead])
# def get_all_roles_perms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     all_roles_perms = actions.get_all_roles_perm(db=db, skip=skip, limit=limit)
#     return all_roles_perms

# # ## endpoint to update the 
# # @role_perm_router.put("/roles-perm/{role_id}", dependencies=[Depends(check_if_is_super_admin)])
# # async def update_roles_perm(role_id: UUID4, db: Session = Depends(get_db)):
# #     update_role_perm = rolePermBaseActions.update_role_perm(role_id=role_id, db=db)
# #     return update_role_perm

# # ## endpoint to update the 
# # @role_perm_router.delete("/roles-perm/{role_id}", dependencies=[Depends(check_if_is_super_admin)])
# # async def delete_roles_perm():
# #     return {"message": "This is role-perm was deleted."}