from typing import Any, List
from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal_cycle as schemas
from domains.appraisal.services.appraisal_cycle import appraisal_cycle_service as actions
from db.session import get_db
from utils import rbac as UserRolesManager


appraisal_cycles_router = APIRouter(
       prefix="/appraisal_cycles",
    tags=["Appraisal Cycle"],
    responses={404: {"description": "Not found"}},
)





@appraisal_cycles_router.get(
    "/all",
    response_model=List[schemas.AppraisalCycleSchema]
)
def list_appraisal_cycles(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    appraisal_cycles_router = actions.list_appraisal_cycle(db=db, skip=skip, limit=limit)
    return appraisal_cycles_router


@appraisal_cycles_router.get(
    "/search",
    response_model=List[schemas.AppraisalCycleSchema]
)
def search_appraisal_cycles_by_name_or_by_year(
        db: Session = Depends(get_db),
        search_word: str = Query(...)
) -> Any:
    appraisal_cycles_router = actions.read_appraisal_cycle_by_name_by_year(db=db, search_word=search_word)
    return appraisal_cycles_router


@appraisal_cycles_router.post(
    "/new",
    response_model=schemas.AppraisalCycleSchema,
    status_code=HTTP_201_CREATED
)
def create_appraisal_cycles(
        *, db: Session = Depends(get_db),
        appraisal_cycles_in: schemas.AppraisalCycleCreate,
         current_user=Depends(UserRolesManager.check_if_user_is_supervisor_or_hr)
) -> Any:
    appraisal_cycles = actions.create_appraisal_cycle(db=db, payload=appraisal_cycles_in)
    return appraisal_cycles


@appraisal_cycles_router.put(
    "/{id}",
    response_model=schemas.AppraisalCycleSchema
)
def update_appraisal_cycles(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        appraisal_cycles_in: schemas.AppraisalCycleUpdate,
) -> Any:
    appraisal_cycles_router = actions.get_appraisal_cycle(db=db, id=id)
    if not appraisal_cycles_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_cycles_router not found"
        )
    appraisal_cycles_router = actions.update_appraisal_cycle(db=db, id=appraisal_cycles_router.id, appraisal_cycle=appraisal_cycles_in)
    return appraisal_cycles_router


@appraisal_cycles_router.get(
    "/{id}",
    response_model=schemas.AppraisalCycleSchema
)
def get_appraisal_cycles(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_cycles_router = actions.get_appraisal_cycle(db=db, id=id)
    if not appraisal_cycles_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_cycles_router not found"
        )
    return appraisal_cycles_router


@appraisal_cycles_router.delete(
    "/{id}",
    response_model=schemas.AppraisalCycleSchema
)
def delete_appraisal_cycles(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_cycles_router = actions.get_appraisal_cycle(db=db, id=id)
    if not appraisal_cycles_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_cycles_router not found"
        )
    appraisal_cycles_router = actions.delete_appraisal_cycle(db=db, id=id)
    return appraisal_cycles_router
