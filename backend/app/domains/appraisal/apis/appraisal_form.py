from typing import Any, List,Union,Annotated
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal_form as schemas
from domains.appraisal.services.appraisal_form import appraisal_form_service as actions
from db.session import get_db
from domains.auth.models.users import User
from utils import rbac



appraisal_form_router = APIRouter(
       prefix="/appraisal_form",
    tags=["appraisal_form"],
    responses={404: {"description": "Not found"}},
)





@appraisal_form_router.get(
    "/",
    response_model=List[schemas.AppraisalFormSchema]
)
def list_appraisal_form(
        db: Session = Depends(get_db),

        skip: int = 0,
        limit: int = 100
) -> Any:
    appraisal_form_router = actions.list_appraisal_form(db=db, skip=skip, limit=limit)
    return appraisal_form_router






@appraisal_form_router.post(
    "/",
    response_model=Union[schemas.AppraisalFormSchema, List[schemas.AppraisalFormSchema]],
)
async def create_appraisal_form(*, db: Session = Depends(get_db), 
                                payload:Union[schemas.AppraisalFormCreate, List[schemas.AppraisalFormCreate]],
                                current_user: Annotated[User, Depends(rbac.get_current_user)]
                                ):

    create_appraisal_form = actions.create_appraisal_form(current_user,db, payload)

    return create_appraisal_form







@appraisal_form_router.put(
    "/{id}",
    response_model=schemas.AppraisalFormSchema
)
def update_appraisal_form(
        *, db: Session = Depends(get_db),

        id: UUID4,
        appraisal_form_in: schemas.AppraisalFormUpdate,
) -> Any:
    appraisal_form_router = actions.get_appraisal_form(db=db, id=id)
    if not appraisal_form_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_form_router not found"
        )
    appraisal_form_router = actions.update_appraisal_form(db=db, id=appraisal_form_router.id, appraisal_form=appraisal_form_in)
    return appraisal_form_router




@appraisal_form_router.get(
    "/{id}",
    response_model=schemas.AppraisalFormSchema
)
def get_appraisal_form_by_id(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    get_appraisal_form_by_id = actions.get_appraisal_form_by_id(db=db, id=id)
    if not get_appraisal_form_by_id:
        data = []
        return {
            "data": data
        }
    return get_appraisal_form_by_id





@appraisal_form_router.delete(
    "/{id}",
    response_model=schemas.AppraisalFormSchema
)
def delete_appraisal_form(
        *, db: Session = Depends(get_db),

        id: UUID4
) -> Any:
    appraisal_form_router = actions.get_appraisal_form(db=db, id=id)
    if not appraisal_form_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_form_router not found"
        )
    appraisal_form_router = actions.delete_appraisal_form(db=db, id=id)
    return appraisal_form_router