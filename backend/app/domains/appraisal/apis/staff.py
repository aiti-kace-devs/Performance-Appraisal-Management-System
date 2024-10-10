from typing import Any, List,Annotated
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import staff as schemas
from domains.appraisal.services.staff import staff_service as actions
from db.session import get_db
from utils import rbac
from domains.auth.models.users import User



staff_router = APIRouter(
       prefix="/staff",
    tags=["staff"],
    responses={404: {"description": "Not found"}},
)





@staff_router.get(
    "/",
    #response_model=List[schemas.StaffWithFullNameInDBBase]
)
async def list_staff(
        current_user: Annotated[User, Depends(rbac.get_current_user)],
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    staff_router = await actions.list_staff(db=db, skip=skip, limit=limit)
    return staff_router


@staff_router.post(
    "/",
    # response_model=schemas.StaffResponse,
    status_code=HTTP_201_CREATED
)
async def create_staff(
        *, db: Session = Depends(get_db),
        staff_in: schemas.StaffCreate,
        current_user: Annotated[User, Depends(rbac.get_current_user)],
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
        current_user: Annotated[User, Depends(rbac.get_current_user)],
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
        id: UUID4,
        current_user: Annotated[User, Depends(rbac.get_current_user)],
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
        id: UUID4,
        current_user: Annotated[User, Depends(rbac.get_current_user)],
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
        name: str,
        current_user: Annotated[User, Depends(rbac.get_current_user)],
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
    current_user: Annotated[User, Depends(rbac.get_current_user)],
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    get_supervisors_router = actions.get_supervisors(db=db, skip=skip, limit=limit)
    return get_supervisors_router








@staff_router.get("/email/{email}",)
def check_staff_email_if_exist(
        *, db: Session = Depends(get_db),
        email: str,
        current_user: Annotated[User, Depends(rbac.get_current_user)],
) -> Any:
    data = actions.check_staff_email_if_exist(db=db, email=email)
    if data:
        return  True
    return False