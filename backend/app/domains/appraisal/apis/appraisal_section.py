from typing import Any, List
from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal_section as schemas
from domains.appraisal.services.appraisal_section import appraisal_section_service as actions
from db.session import get_db


appraisal_sections_router = APIRouter(
       prefix="/appraisal_sections",
    tags=["Appraisal Section"],
    responses={404: {"description": "Not found"}},
)





@appraisal_sections_router.get(
    "/all",
    response_model=List[schemas.AppraisalSectionSchema]
)
def list_appraisal_sections(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    appraisal_sections_router = actions.list_appraisal_section(db=db, skip=skip, limit=limit)
    return appraisal_sections_router


# @appraisal_sections_router.get(
#     "/search",
#     response_model=List[schemas.AppraisalSectionSchema]
# )
# def search_appraisal_sections_by_name_or_by_year(
#         db: Session = Depends(get_db),
#         search_word: str = Query(...)
# ) -> Any:
#     appraisal_sections_router = actions.read_appraisal_section_by_name_by_year(db=db, search_word=search_word)
#     return appraisal_sections_router


@appraisal_sections_router.post(
    "/new",
    response_model=schemas.AppraisalSectionSchema,
)
def create_appraisal_sections(
        *, db: Session = Depends(get_db),
        # 
        appraisal_sections_in: schemas.AppraisalSectionCreate
) -> Any:
    appraisal_sections_router = actions.create_appraisal_section(db=db, payload=appraisal_sections_in)
    return appraisal_sections_router


@appraisal_sections_router.put(
    "/{id}",
    response_model=schemas.AppraisalSectionSchema
)
def update_appraisal_sections(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        appraisal_sections_in: schemas.AppraisalSectionUpdate,
) -> Any:
    appraisal_sections_router = actions.get_appraisal_section(db=db, id=id)
    if not appraisal_sections_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_sections_router not found"
        )
    appraisal_sections_router = actions.update_appraisal_section(db=db, id=appraisal_sections_router.id, appraisal_section=appraisal_sections_in)
    return appraisal_sections_router


@appraisal_sections_router.get(
    "/{id}",
    response_model=schemas.AppraisalSectionSchema
)
def get_appraisal_sections(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_sections_router = actions.get_appraisal_section(db=db, id=id)
    if not appraisal_sections_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_sections_router not found"
        )
    return appraisal_sections_router


@appraisal_sections_router.delete(
    "/{id}",
    response_model=schemas.AppraisalSectionSchema
)
def delete_appraisal_sections(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_sections_router = actions.get_appraisal_section(db=db, id=id)
    if not appraisal_sections_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_sections_router not found"
        )
    appraisal_sections_router = actions.delete_appraisal_section(db=db, id=id)
    return appraisal_sections_router
