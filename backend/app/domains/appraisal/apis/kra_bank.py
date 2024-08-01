from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import kra_bank as schemas
from domains.appraisal.services.kra_bank import kra_bank_form_service as actions
from db.session import get_db


kra_bank_router = APIRouter(
       prefix="/kra_bank",
    tags=["KRA Bank"],
    responses={404: {"description": "Not found"}},
)





@kra_bank_router.get(
    "/",
    response_model=List[schemas.KraBankSchema]
)
def list_kra_bank(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    kra_bank_router = actions.list_kra_bank_form(db=db, skip=skip, limit=limit)
    return kra_bank_router


@kra_bank_router.post(
    "/",
    response_model=schemas.KraBankSchema,
    status_code=HTTP_201_CREATED
)
def create_kra_bank(
        *, db: Session = Depends(get_db),
        # 
        kra_bank_in: schemas.KraBankCreate
) -> Any:
    kra_bank_router = actions.create_kra_bank_form(db=db, kra_bank=kra_bank_in)
    return kra_bank_router


@kra_bank_router.put(
    "/{id}",
    response_model=schemas.KraBankSchema
)
def update_appraisal_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        kra_bank_in: schemas.KraBankUpdate,
) -> Any:
    kra_bank_router = actions.get_kra_bank_form(db=db, id=id)
    if not kra_bank_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="kra_bank_router not found"
        )
    kra_bank_router = actions.update_kra_bank_form(db=db, id=kra_bank_router.id, kra_bank_in=kra_bank_in)
    return kra_bank_router


@kra_bank_router.get(
    "/{id}",
    response_model=schemas.KraBankSchema
)
def get_kra_bank(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    kra_bank_router = actions.get_kra_bank_form(db=db, id=id)
    if not kra_bank_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="kra_bank_router not found"
        )
    return kra_bank_router


@kra_bank_router.delete(
    "/{id}",
    response_model=schemas.KraBankSchema
)
def delete_kra_bank(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    kra_bank_router = actions.get_kra_bank_form(db=db, id=id)
    if not kra_bank_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="kra bank router not found"
        )
    kra_bank_router = actions.delete_kra_bank_form(db=db, id=id)
    return kra_bank_router



