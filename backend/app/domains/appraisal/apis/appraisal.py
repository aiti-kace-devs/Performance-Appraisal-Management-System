from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal as schemas
from domains.appraisal.services.appraisal import appraisal_service as actions
from db.session import get_db


appraisals_router = APIRouter(
       prefix="/appraisals",
    tags=["Appraisal Form"],
    responses={404: {"description": "Not found"}},
)





@appraisals_router.get(
    "/",
    response_model=List[schemas.AppraisalSchema]
)
def list_appraisals(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    appraisals_router = actions.list_appraisal(db=db, skip=skip, limit=limit)
    return appraisals_router


@appraisals_router.post(
    "/",
    response_model=schemas.AppraisalSchema,
    status_code=HTTP_201_CREATED
)
def create_appraisals(
        *, db: Session = Depends(get_db),
        # 
        appraisals_in: schemas.AppraisalCreate
) -> Any:
    appraisals_router = actions.create_appraisal(db=db, appraisal=appraisals_in)
    return appraisals_router


@appraisals_router.put(
    "/{id}",
    response_model=schemas.AppraisalSchema
)
def update_appraisals(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        appraisals_in: schemas.AppraisalUpdate,
) -> Any:
    appraisals_router = actions.get_appraisal(db=db, id=id)
    if not appraisals_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisals_router not found"
        )
    appraisals_router = actions.update_appraisal(db=db, id=appraisals_router.id, appraisals_in=appraisals_in)
    return appraisals_router


@appraisals_router.get(
    "/{id}",
    response_model=schemas.AppraisalSchema
)
def get_appraisals(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisals_router = actions.get_appraisal(db=db, id=id)
    if not appraisals_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisals_router not found"
        )
    return appraisals_router


@appraisals_router.delete(
    "/{id}",
    response_model=schemas.AppraisalSchema
)
def delete_appraisals(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisals_router = actions.get_appraisal(db=db, id=id)
    if not appraisals_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisals_router not found"
        )
    appraisals_router = actions.delete_appraisal(db=db, id=id)
    return appraisals_router
