from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import staff_deadline as schemas
from domains.appraisal.services.staff_deadline import staff_deadline_service as actions
from db.session import get_db


staff_deadline_router = APIRouter(
       prefix="/staff_deadlines",
    tags=["Staff Deadline"],
    responses={404: {"description": "Not found"}},
)





@staff_deadline_router.get(
    "/",
    response_model=List[schemas.StaffDeadlineSchema]
)
def list_staff_deadline(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    list_staff_deadline = actions.list_staff_deadline(db=db, skip=skip, limit=limit)
    return list_staff_deadline


@staff_deadline_router.post(
    "/",
    response_model=schemas.StaffDeadlineSchema,
    status_code=HTTP_201_CREATED
)
def create_staff_deadline(
        *, db: Session = Depends(get_db),
        # 
        staff_deadline_in: schemas.StaffDeadlineCreate
) -> Any:
    create_staff_deadline = actions.create_staff_deadline(db=db, staff_deadline=staff_deadline_in)
    return create_staff_deadline


@staff_deadline_router.put(
    "/{id}",
    response_model=schemas.StaffDeadlineSchema
)
def update_staff_deadline(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        staff_deadline_in: schemas.StaffDeadlineUpdate,
) -> Any:
    get = actions.get_staff_deadline_by_id(db=db, id=id)
    if not get:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff deadline router not found"
        )
    update_staff_deadline = actions.update_staff_deadline(db=db, id=get.id, staff_deadline=staff_deadline_in)
    return update_staff_deadline


@staff_deadline_router.get(
    "/{id}",
    response_model=schemas.StaffDeadlineSchema
)
def get_staff_deadline(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    get_staff_deadline = actions.get_staff_deadline_by_id(db=db, id=id)
    if not get_staff_deadline:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff deadline router not found"
        )
    return get_staff_deadline


@staff_deadline_router.delete(
    "/{id}",
    response_model=schemas.StaffDeadlineSchema
)
def delete_staff_deadline(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    get_staff_deadline2 = actions.get_staff_deadline_by_id(db=db, id=id)
    if not get_staff_deadline2:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff deadline router not found"
        )
    delete_staff_deadline = actions.delete_staff_deadline(db=db, id=id)
    return delete_staff_deadline
