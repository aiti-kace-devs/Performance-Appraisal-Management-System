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
    tags=["Satff Appraisal"],
    responses={404: {"description": "Not found"}},
)





@appraisals_router.get(
    "/{staff_id}/{appraisal_cycle_id}",
    response_model=schemas.GetStaffAppraisalBase
)
def get_staff_appraisals_by_staff_id(
    staff_id: UUID4,
    appraisal_cycle_id: UUID4,
    db: Session = Depends(get_db)
         
):
    appraisals_router = actions.get_appraisal_by_id(db=db, staff_id=staff_id, appraisal_cycle_id=appraisal_cycle_id)
    return appraisals_router











@appraisals_router.get(
    "/{staff_id}//{appraisal_cycle_id}/{appraisal_year}",
)
def get_staff_appraisals_by_staff_id_and_appraisal_year(
    staff_id: UUID4,
    appraisal_cycle_id: UUID4,
    appraisal_year: int,
    db: Session = Depends(get_db)
         
):
    appraisals_router = actions.get_staff_appraisals_by_staff_id_and_appraisal_year(db=db, staff_id=staff_id, appraisal_cycle_id=appraisal_cycle_id, appraisal_year=appraisal_year)
    return appraisals_router