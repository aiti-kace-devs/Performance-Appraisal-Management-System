from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import users as schemas
from domains.appraisal.services.users import users_forms_service as actions
from db.session import get_db


users_router = APIRouter(
       prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)





@users_router.get(
    "/",
    response_model=List[schemas.UserSchema]
)
def list_users_forms(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    users_router = actions.list_users_forms(db=db, skip=skip, limit=limit)
    return users_router


@users_router.post(
    "/",
    response_model=schemas.UserSchema,
    status_code=HTTP_201_CREATED
)
def create_users_forms(
        *, db: Session = Depends(get_db),
        # 
        users_forms_in: schemas.UserCreate
) -> Any:
    users_router = actions.create_users_forms(db=db, users_forms=users_forms_in)
    return users_router


@users_router.put(
    "/{id}",
    response_model=schemas.UserSchema
)
def update_users_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        users_forms_in: schemas.UserUpdate,
) -> Any:
    users_router = actions.get_users_forms(db=db, id=id)
    if not users_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="users_forms_router not found"
        )
    users_router = actions.update_users_forms(db=db, id=users_router.id, users_forms_in=users_forms_in)
    return users_router


@users_router.get(
    "/{id}",
    response_model=schemas.UserSchema
)
def get_users_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    users_router = actions.get_users_forms(db=db, id=id)
    if not users_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="users_forms_router not found"
        )
    return users_router


@users_router.delete(
    "/{id}",
    response_model=schemas.UserSchema
)
def delete_users_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    users_forms_router = actions.get_users_forms(db=db, id=id)
    if not users_forms_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="users_forms_router not found"
        )
    users_router = actions.delete_users_forms(db=db, id=id)
    return users_router
