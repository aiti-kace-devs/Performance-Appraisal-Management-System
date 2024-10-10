from typing import Any, List,Annotated
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from utils import rbac as UserRolesManager
from domains.appraisal.schemas.roles import RoleCreate, RoleUpdate, RoleRead
from domains.appraisal.services.role import role_service as actions 
from utils import rbac
from domains.auth.models.users import User

# from domains.appraisal.schemas import appraisal as schemas
# from domains.appraisal.services.appraisal import appraisal_form_service as actions

from db.session import get_db



# APIRouter creates path operations for admin and users module
role_router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
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
@role_router.get("/{id}", response_model=RoleRead)
def get_row(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    role = actions.get_role_by_id(db=db, role_id=id)
    if not role:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="role not found"
        )
    return role 

## endpoint to 
@role_router.get("/", response_model=List[RoleRead])
def get_all_roles(*, db: Session = Depends(get_db), 
                  current_user: Annotated[User, Depends(rbac.get_current_user)],
                  skip: int=0, limit: int=0, 
                  
                  ):
    all_roles = actions.get_all_roles(db=db)
    return all_roles 

## endpoint to get current user 

@role_router.put("/{role_id}", response_model=RoleUpdate)
def update_role(role_id: UUID4, role_update: RoleUpdate, db: Session = Depends(get_db)):
    role_update = actions.updated_role(db, role_id, role_update)
    return role_update
