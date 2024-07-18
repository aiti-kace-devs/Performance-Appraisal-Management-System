from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal as schemas
from domains.appraisal.services.appraisal import appraisal_form_service as actions
from db.session import get_db


appraisal_forms_router = APIRouter(
       prefix="/appraisal_forms",
    tags=["Appraisal Form"],
    responses={404: {"description": "Not found"}},
)





@appraisal_forms_router.get(
    "/",
    response_model=List[schemas.AppraisalSchema]
)
def list_appraisal_forms(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    appraisal_forms_router = actions.list_appraisal_form(db=db, skip=skip, limit=limit)
    return appraisal_forms_router


@appraisal_forms_router.post(
    "/",
    response_model=schemas.AppraisalSchema,
    status_code=HTTP_201_CREATED
)
def create_appraisal_forms(
        *, db: Session = Depends(get_db),
        # 
        appraisal_forms_in: schemas.AppraisalCreate
) -> Any:
    appraisal_forms_router = actions.create_appraisal_form(db=db, appraisal_form=appraisal_forms_in)
    return appraisal_forms_router


@appraisal_forms_router.put(
    "/{id}",
    response_model=schemas.AppraisalSchema
)
def update_appraisal_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        appraisal_forms_in: schemas.AppraisalUpdate,
) -> Any:
    appraisal_forms_router = actions.get_appraisal_form(db=db, id=id)
    if not appraisal_forms_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_forms_router not found"
        )
    appraisal_forms_router = actions.update_appraisal_form(db=db, id=appraisal_forms_router.id, appraisal_forms_in=appraisal_forms_in)
    return appraisal_forms_router


@appraisal_forms_router.get(
    "/{id}",
    response_model=schemas.AppraisalSchema
)
def get_appraisal_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_forms_router = actions.get_appraisal_form(db=db, id=id)
    if not appraisal_forms_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_forms_router not found"
        )
    return appraisal_forms_router


@appraisal_forms_router.delete(
    "/{id}",
    response_model=schemas.AppraisalSchema
)
def delete_appraisal_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_forms_router = actions.get_appraisal_form(db=db, id=id)
    if not appraisal_forms_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_forms_router not found"
        )
    appraisal_forms_router = actions.delete_appraisal_form(db=db, id=id)
    return appraisal_forms_router
