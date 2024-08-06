from typing import Any, List
from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import staff_permissions as schemas
from domains.appraisal.services.staff_permissions import staff_permission_service as actions
from db.session import get_db


staff_permission_router = APIRouter(
       prefix="/staff_permissions",
    tags=["Staff Permission"],
    responses={404: {"description": "Not found"}},
)

@staff_permission_router.post(
    "/new",
    response_model=schemas.StaffPermissionSchema,
    status_code=HTTP_201_CREATED
)
def create_staff_permission(
        *, db: Session = Depends(get_db),
        staff_permission_in: schemas.StaffPermissionCreate
) -> Any:
    staff_permission_router = actions.create_staff_permissions(db=db, staff_permission = staff_permission_in)
    return staff_permission_router

@staff_permission_router.get(
    "/all",
    response_model=List[schemas.StaffPermissionSchema]
)
def get_all_staff_permissions(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> Any:
    staff_permission_router = actions.get_all_staff_permissions(db=db, skip=skip, limit=limit)
    return staff_permission_router

@staff_permission_router.get(
    "/{id}",
    response_model=schemas.StaffPermissionSchema
)
def get_staff_permission(
        *, db: Session = Depends(get_db),
        id: UUID4
) -> Any:
    staff_permission_router = actions.get_staff_permissions(db=db, id=id)
    if not staff_permission_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff_permission_router not found"
        )
    return staff_permission_router

@staff_permission_router.put(
    "/{id}",
    response_model=schemas.StaffPermissionSchema
)
def update_staff_permissions(
        *, db: Session = Depends(get_db),
        id: UUID4,
        staff_permissions_in: schemas.StaffPermissionUpdate,
) -> Any:
    staff_permission_router = actions.get_staff_permissions(db=db, id=id)
    if not staff_permission_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff_permission_router not found"
        )
    staff_permission_router = actions.update_staff_permissions(db=db, db_obj= staff_permission_router,  obj_in = staff_permissions_in)
    return staff_permission_router

@staff_permission_router.delete(
    "/{id}",
    response_model=schemas.StaffPermissionSchema
)
def delete_staff_permission(
        *, db: Session = Depends(get_db),

        id: UUID4
) -> Any:
    staff_permission_router = actions.get_staff_permissions(db=db, id=id)
    if not staff_permission_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="staff_permission_router not found"
        )
    staff_permission_router = actions.delete_staff_permissions(db=db, id=id)
    return staff_permission_router
