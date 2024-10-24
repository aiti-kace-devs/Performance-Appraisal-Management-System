from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from domains.appraisal.schemas.permissions import PermissionRead
from domains.appraisal.services.permission import perm_service as actions



from db.session import get_db



# APIRouter creates path operations for admin and users module
perm_router = APIRouter(
    prefix="/perms",
    tags=["Permission"],
    responses={404: {"description": "Not found"}},
)

# def get_current_user_role(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     user_id = decode_access_token(token)
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return user.role

# def check_roles(roles: List[str]):
#     def role_checker(role: Role = Depends(get_current_user_role)):
#         if role.name not in roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Operation not permitted"
#             )
#     return role_checker

# ## create a new role 
# @role_router.post("/", response_model= RoleRead)
# def create_new_role_permission(*, payload: RoleCreate, db:Session=Depends(get_db)):
#     new_role_perm = actions.create_role_perm(role_perm=payload, db=db)
#     return new_role_perm


## get role by the row_id 
@perm_router.get("/{id}", response_model=PermissionRead)
def get_perm(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    perm = actions.get_perm_by_id(db=db, perm_id=id)
    if not perm:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="role not found"
        )
    return perm

## endpoint to 
@perm_router.get("/", response_model=List[PermissionRead])
def get_all_perms(*, db: Session = Depends(get_db), skip: int=0, limit: int=0):
    all_perms = actions.get_all_perms(db=db)
    return all_perms

## endpoint to get current user 
