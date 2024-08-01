from typing import Any, List
from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal_configuration as schemas
from domains.appraisal.services.appraisal_configuration import appraisal_configuration_service as actions
from db.session import get_db


appraisal_configuration_router = APIRouter(
       prefix="/appraisal_configuration",
    tags=["Appraisal Configuration"],
    responses={404: {"description": "Not found"}},
)





@appraisal_configuration_router.get(
    "/all",
    response_model=List[schemas.AppraisalConfigurationSchema]
)
def list_appraisal_configuration(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    appraisal_configuration_router = actions.list_appraisal_configuration(db=db, skip=skip, limit=limit)
    return appraisal_configuration_router


@appraisal_configuration_router.get(
    "/search"
)
def search_appraisal_configuration_by_keyword(
        db: Session = Depends(get_db),
        search_word: str = Query(...)
) -> Any:
    result = actions.get_appraisal_configuration_by_keywords(db=db, tag=search_word)
    #return result
    if isinstance(result, list):
        return result
    return [result]


@appraisal_configuration_router.post(
    "/new",
    response_model=schemas.AppraisalConfigurationSchema,
    status_code=HTTP_201_CREATED
)
def create_appraisal_configuration(
        *, db: Session = Depends(get_db),
        # 
        appraisal_configuration_in: schemas.AppraisalConfigurationCreate
) -> Any:
    appraisal_configuration_router = actions.create_appraisal_configuration(db=db, appraisal_configuration=appraisal_configuration_in)
    return appraisal_configuration_router


@appraisal_configuration_router.put(
    "/{id}",
    response_model=schemas.AppraisalConfigurationSchema
)
def update_appraisal_configuration(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        appraisal_configuration_in: schemas.AppraisalConfigurationUpdate,
) -> Any:
    appraisal_configuration_router = actions.get_appraisal_configuration(db=db, id=id)
    if not appraisal_configuration_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_configuration_router not found"
        )
    appraisal_configuration_router = actions.update_appraisal_configuration(db=db, id=appraisal_configuration_router.id, appraisal_configuration=appraisal_configuration_in)
    return appraisal_configuration_router


@appraisal_configuration_router.get(
    "/{id}",
    response_model=schemas.AppraisalConfigurationSchema
)
def get_appraisal_configuration(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_configuration_router = actions.get_appraisal_configuration(db=db, id=id)
    if not appraisal_configuration_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_configuration_router not found"
        )
    return appraisal_configuration_router


@appraisal_configuration_router.delete(
    "/{id}",
    response_model=schemas.AppraisalConfigurationSchema
)
def delete_appraisal_configuration(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_configuration_router = actions.get_appraisal_configuration(db=db, id=id)
    if not appraisal_configuration_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_configuration_router not found"
        )
    appraisal_configuration_router = actions.delete_appraisal_configuration(db=db, id=id)
    return appraisal_configuration_router
