from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal_submission as schemas
from domains.appraisal.services.appraisal_submission import appraisal_submission_service as actions
from db.session import get_db


appraisal_submissions_router = APIRouter(
       prefix="/appraisal_submissions",
    tags=["Appraisal Submission"],
    responses={404: {"description": "Not found"}},
)





@appraisal_submissions_router.get(
    "/",
    response_model=List[schemas.AppraisalSubmissionSchema]
)
def list_appraisal_submissions(
        db: Session = Depends(get_db),
        
        skip: int = 0,
        limit: int = 100
) -> Any:
    appraisal_submissions_router = actions.list_appraisal_submission(db=db, skip=skip, limit=limit)
    return appraisal_submissions_router


@appraisal_submissions_router.post(
    "/",
    response_model=schemas.AppraisalSubmissionSchema,
    status_code=HTTP_201_CREATED
)
def create_appraisal_submissions(
        *, db: Session = Depends(get_db),
        # 
        appraisal_submissions_in: schemas.AppraisalSubmissionCreate
) -> Any:
    appraisal_submissions_router = actions.create_appraisal_submission(db=db, appraisal_submission=appraisal_submissions_in)
    return appraisal_submissions_router


@appraisal_submissions_router.put(
    "/{id}",
    response_model=schemas.AppraisalSubmissionSchema
)
def update_appraisal_submissions(
        *, db: Session = Depends(get_db),
        
        id: UUID4,
        appraisal_submissions_in: schemas.AppraisalSubmissionUpdate,
) -> Any:
    appraisal_submissions_router = actions.get_appraisal_submission(db=db, id=id)
    if not appraisal_submissions_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_submissions_router not found"
        )
    appraisal_submissions_router = actions.update_appraisal_submission(db=db, id=appraisal_submissions_router.id, appraisal_submission=appraisal_submissions_in)
    return appraisal_submissions_router


@appraisal_submissions_router.get(
    "/{id}",
    response_model=schemas.AppraisalSubmissionSchema
)
def get_appraisal_submissions(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_submissions_router = actions.get_appraisal_submission(db=db, id=id)
    if not appraisal_submissions_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_submissions_router not found"
        )
    return appraisal_submissions_router


@appraisal_submissions_router.delete(
    "/{id}",
    response_model=schemas.AppraisalSubmissionSchema
)
def delete_appraisal_submissions(
        *, db: Session = Depends(get_db),
        
        id: UUID4
) -> Any:
    appraisal_submissions_router = actions.get_appraisal_submission(db=db, id=id)
    if not appraisal_submissions_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="appraisal_submissions_router not found"
        )
    appraisal_submissions_router = actions.delete_appraisal_submission(db=db, id=id)
    return appraisal_submissions_router
