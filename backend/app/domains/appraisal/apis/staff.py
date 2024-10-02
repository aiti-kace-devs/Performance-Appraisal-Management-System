from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import staff as schemas
from domains.appraisal.services.staff import staff_service as actions
from db.session import get_db


staff_router = APIRouter(
       prefix="/staff",
    tags=["staff"],
    responses={404: {"description": "Not found"}},
)





@staff_router.get(
    "/",
    response_model=List[schemas.StaffWithFullNameInDBBase]
)
async def list_staff(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    staff_router = await actions.list_staff(db=db, skip=skip, limit=limit)
    return staff_router


@staff_router.post(
    "/",
    status_code=HTTP_201_CREATED
)
async def create_staff(
        *, db: Session = Depends(get_db),
        # 
        staff_in: schemas.StaffCreate
) -> Any:
    staff_router = await actions.create_staff(db=db, staff=staff_in)

    return staff_router


@staff_router.put(
    "/{id}",
)
def update_staff(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        staff_in: schemas.StaffUpdate,
) -> Any:
    staff_router = actions.get_staff_by_id(db=db, id=id)
    if not staff_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff_router not found"
        )
    staff_router =  actions.update_staff(db=db, id=staff_router.get('id'), staff=staff_in)
    return staff_router


@staff_router.get(
    "/{id}"
    )
def get_staff(
        *, db: Session = Depends(get_db),
        id: UUID4
) -> Any:
    staff_router = actions.get_staff_by_id(db=db, id=id)
    if not staff_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff not found"
        )
    return staff_router


@staff_router.delete(
    "/{id}"
)
def delete_staff(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    staff_router = actions.get_staff_by_id(db=db, id=id)
    if not staff_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff_router not found"
        )
    staff_router = actions.delete_staff(db=db, id=id)
    return staff_router











@staff_router.get("/search/{name}",)
def search_staff(
        *, db: Session = Depends(get_db),
        name: str
) -> Any:
    search_staff = actions.search_staff(db=db, name=name)
    if not search_staff:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff not found"
        )
    return search_staff





@staff_router.get(
    "/supervisors/",
    response_model=List[schemas.StaffWithFullNameInDBBase]
)
async def list_supervisors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    get_supervisors_router = actions.get_supervisors(db=db, skip=skip, limit=limit)
    return get_supervisors_router