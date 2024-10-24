from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.appraisal import appraisal_form_actions as appraisal_repo
from domains.appraisal.schemas.appraisal import AppraisalSchema, AppraisalUpdate, AppraisalCreate
from domains.appraisal.models.appraisal_cycle import AppraisalCycle
from domains.appraisal.models.staff import Staff


class AppraisalService:


    def list_appraisal(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalSchema]:
        appraisal = appraisal_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal

    def create_appraisal(self, *, db: Session, appraisal: AppraisalCreate) -> AppraisalSchema:

        check_appraisal_cycle_id = db.query(AppraisalCycle).filter(AppraisalCycle.id == appraisal.appraisal_cycles_id).first()
        if not check_appraisal_cycle_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Appraisal cycle not found")
        
        check_staff_id = db.query(Staff).filter(Staff.id == appraisal.staff_id).first()
        if not check_staff_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Staff not found")
        
        check_supervisor_id = db.query(Staff).filter(Staff.id == appraisal.supervisor_id).first()
        if not check_supervisor_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Supervisor not found")

        appraisal = appraisal_repo.create(db=db, obj_in=appraisal)
        return appraisal

    def update_appraisal(self, *, db: Session, id: UUID, appraisal: AppraisalUpdate) -> AppraisalSchema:
        appraisal_ = appraisal_repo.get(db=db, id=id)
        if not appraisal_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal not found")
        appraisal = appraisal_repo.update(db=db, db_obj=appraisal_, obj_in=appraisal)
        return appraisal

    def get_appraisal(self, *, db: Session, id: UUID) -> AppraisalSchema:
        appraisal = appraisal_repo.get(db=db, id=id)
        if not appraisal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal not found")
        return appraisal

    def delete_appraisal(self, *, db: Session, id: UUID) -> AppraisalSchema:
        appraisal = appraisal_repo.get(db=db, id=id)
        if not appraisal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal not found")
        appraisal = appraisal_repo.remove(db=db, id=id)
        return appraisal

    def get_appraisal_by_id(self, *, id: UUID) -> AppraisalSchema:
        appraisal = appraisal_repo.get(id)
        if not appraisal:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="appraisal not found"
            )
        return appraisal

    def get_appraisal_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalSchema]:
        pass

    def search_appraisal(self, *, db: Session, search: str, value: str) -> List[AppraisalSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return appraisal_repo.get_by_kwargs(self, db, kwargs)


appraisal_service = AppraisalService()