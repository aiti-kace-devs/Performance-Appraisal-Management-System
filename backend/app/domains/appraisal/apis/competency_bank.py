from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import competency_bank as schemas
from domains.appraisal.services.competency_bank import competency_bank_form_service as actions
from db.session import get_db
from typing import Union,List

competency_bank_forms_router = APIRouter(
       prefix="/competency_banks",
    tags=["Competency Bank"],
    responses={404: {"description": "Not found"}},
)





@competency_bank_forms_router.get(
    "/",
    response_model=List[schemas.CompetencyBankSchema]
)
def list_competency_bank_forms(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    competency_bank_forms_router = actions.list_competency_bank_form(db=db, skip=skip, limit=limit)
    return competency_bank_forms_router


# @competency_bank_forms_router.post(
#     "/",
#     #response_model=schemas.CompetencyBankSchema,
#     status_code=HTTP_201_CREATED
# )
# def create_competency_bank_forms(
#         *, db: Session = Depends(get_db),
#         # 
#         competency_bank_forms_in: schemas.CompetencyBankCreate
# ) -> Any:
#     competency_bank_forms_router = actions.create_competency_bank_form(db=db, payload=competency_bank_forms_in)
#     return competency_bank_forms_router


@competency_bank_forms_router.post(
    "/",
    #response_model=schemas.CompetencyBankSchema,
    response_model=Union[schemas.CompetencyBankSchema, List[schemas.CompetencyBankSchema]],
    status_code=HTTP_201_CREATED
)
async def create_competency_bank(*, db: Session = Depends(get_db), payload:Union[schemas.CompetencyBankCreate, List[schemas.CompetencyBankCreate]]):

    create_competency_bank = actions.create_competency_bank_form(db, payload)

    return create_competency_bank




@competency_bank_forms_router.put(
    "/{id}",
    response_model=schemas.CompetencyBankSchema
)
def update_competency_bank_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        competency_bank_forms_in: schemas.CompetencyBankUpdate,
) -> Any:
    competency_bank_forms_router = actions.get_competency_bank_form(db=db, id=id)
    if not competency_bank_forms_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="competency_bank_forms_router not found"
        )
    competency_bank_forms_router = actions.update_competency_bank_form(db=db, id=competency_bank_forms_router.id, competency_bank_form=competency_bank_forms_in)
    return competency_bank_forms_router


@competency_bank_forms_router.get(
    "/{id}",
    response_model=schemas.CompetencyBankSchema
)
def get_competency_bank_by_id(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    get_competency_bank_by_id = actions.get_competency_bank_by_id(db=db, id=id)
    if not get_competency_bank_by_id:
        data = []
        return {
            "data": data
        }
    return get_competency_bank_by_id


@competency_bank_forms_router.delete(
    "/{id}",
    response_model=schemas.CompetencyBankSchema
)
def delete_competency_bank_forms(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    competency_bank_forms_router = actions.get_competency_bank_form(db=db, id=id)
    if not competency_bank_forms_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="competency_bank_forms_router not found"
        )
    competency_bank_forms_router = actions.delete_competency_bank_form(db=db, id=id)
    return competency_bank_forms_router
