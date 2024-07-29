from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import competency_bank as schemas
from domains.appraisal.services.competency_bank import competency_bank_form_service as actions
from db.session import get_db

competency_bank_router = APIRouter(
       prefix="/competency-bank",
    tags=["CompentencyBank"],
    responses={404: {"description": "Not found"}},
)





@competency_bank_router.get(
    "/",
    response_model=List[schemas.CompentencyBankSchema]
)
def list_competency_bank_form(
        db: Session = Depends(get_db),

        skip: int = 0,
        limit: int = 100
) -> Any:
    competency_bank_router = actions.list_competency_bank_form(db=db, skip=skip, limit=limit)
    return competency_bank_router


@competency_bank_router.post(
    "/",
    response_model=schemas.CompentencyBankSchema,
    status_code=HTTP_201_CREATED
)
def create_competency_bank_form(
        *, db: Session = Depends(get_db),
        # 
        competency_bank_form_in: schemas.CompentencyBankCreate
) -> Any:
    competency_bank_router = actions.create_competency_bank_form(db=db, competency_bank_form=competency_bank_form_in)
    return competency_bank_router


@competency_bank_router.put(
    "/{id}",
    response_model=schemas.CompentencyBankSchema
)
def update_competency_bank_form(
        *, db: Session = Depends(get_db),

        id: UUID4,
        competency_bank_form_in: schemas.CompentencyBankUpdate,
) -> Any:
    competency_bank_router = actions.get_competency_bank_form(db=db, id=id)
    if not competency_bank_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="competency_bank_form_router not found"
        )
    competency_bank_router = actions.update_competency_bank_form(db=db, id=competency_bank_router.id, competency_bank_form_in=competency_bank_form_in)
    return competency_bank_router


@competency_bank_router.get(
    "/{id}",
    response_model=schemas.CompentencyBankSchema
)
def get_competency_bank_form(
        *, db: Session = Depends(get_db),

        id: UUID4
) -> Any:
    competency_bank_router = actions.get_competency_bank_form(db=db, id=id)
    if not competency_bank_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="competency_bank_form_router not found"
        )
    return competency_bank_router


@competency_bank_router.delete(
    "/{id}",
    response_model=schemas.CompentencyBankSchema
)
def delete_competency_bank_form(
        *, db: Session = Depends(get_db),

        id: UUID4
) -> Any:
    competency_bank_form_router = actions.get_competency_bank_form(db=db, id=id)
    if not competency_bank_form_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="competency_bank_form_router not found"
        )
    competency_bank_router = actions.delete_competency_bank_form(db=db, id=id)
    return competency_bank_router