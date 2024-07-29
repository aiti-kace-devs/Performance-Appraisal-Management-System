from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from domains.appraisal.schemas import roles as schema
from domains.appraisal.services.role import role_service as actions 


# from domains.appraisal.schemas import appraisal as schemas
# from domains.appraisal.services.appraisal import appraisal_form_service as actions

from db.session import get_db



# APIRouter creates path operations for admin and users module
role_router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found"}},
)


# @role_router.post("/roles/", response_model=schema.CreateRole)
# def create_new_role(*, payload: schema.CreateRole, db:Session=Depends(get_db)):
#     new_role = roleBaseActions.create_roles(payload, db)
#     return new_role


@role_router.get("/{id}", response_model=schema.RoleRead)
def get_row(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    role = actions.get_role_by_id(db=db, id=id)
    if not role:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="role not found"
        )
    return role 

## endpoint to 
@role_router.get("/roles", response_model=schema.RoleRead)
def get_all_roles(*, db: Session = Depends(get_db), skip: int=0, limit=10):
    all_roles = actions.get_all_roles(db=db, skip=skip, limit=limit)
    return all_roles 