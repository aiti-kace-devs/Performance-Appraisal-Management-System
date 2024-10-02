from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import department as schemas
from domains.appraisal.services.department import department_service as actions
from db.session import get_db
from domains.appraisal.schemas.staff import StaffSchema,StaffWithFullNameInDBBase

department_router = APIRouter(
       prefix="/department",
    tags=["Department"],
    responses={404: {"description": "Not found"}},
)





@department_router.get(
    "/",
    response_model=List[schemas.DepartmentWithTotalStaff]
)
def list_department(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    department_router = actions.list_department(db=db, skip=skip, limit=limit)
    return department_router


@department_router.post(
    "/",
    response_model=schemas.DepartmentSchema,
    status_code=HTTP_201_CREATED
)
async def create_department(
        *, db: Session = Depends(get_db),
        # 
        department_in: schemas.DepartmentCreate
) -> Any:
    department_router = await actions.create_department(db=db, department=department_in)
    return department_router



@department_router.get(
    "/{id}",
    response_model=schemas.DepartmentSchema
)
def get_department(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    department_router = actions.get_department(db=db, id=id)
    if not department_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="department_router not found"
        )
    return department_router




@department_router.put(
    "/{id}",
    response_model=schemas.DepartmentSchema
)
def update_department(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        department_in: schemas.DepartmentUpdate
) -> Any:
    department_router = actions.get_department(db=db, id=id)
    if not department_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="department_router not found"
        )
    department_router = actions.update_department(db=db, id=department_router.id, department=department_in)
    return department_router





@department_router.get(
    "/staff/{id}",
    response_model=List[StaffWithFullNameInDBBase]
)
def list_all_staff_under_department(
        *, db: Session = Depends(get_db),
        id: UUID4,
        skip: int = 0,
        limit: int = 100
) -> Any:
    list_staff = actions.list_all_staff_under_department(db=db, id=id, skip=skip, limit=limit)
    if not list_staff:
        return []
    return list_staff


@department_router.delete(
    "/{id}",
    response_model=schemas.DepartmentSchema
)
def delete_department(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    department_router = actions.get_department(db=db, id=id)
    if not department_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="department_router not found"
        )
    
    check_if_department_has_staff = actions.check_if_department_has_staff(db, id)

    if check_if_department_has_staff:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="This department has staff members so it cannot be deleted"
        )

    department_router = actions.delete_department(db=db, id=id)
    return department_router
