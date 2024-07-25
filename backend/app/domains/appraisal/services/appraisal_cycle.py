from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.appraisal_cycle import appraisal_cycle_actions as appraisal_cycle_repo
from domains.appraisal.schemas.appraisal_cycle import AppraisalCycleSchema, AppraisalCycleUpdate, AppraisalCycleCreate
from domains.appraisal.models.appraisal_cycle import AppraisalCycle

class AppraisalCycleService:


    def list_appraisal_cycle(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalCycleSchema]:
        appraisal_cycle = appraisal_cycle_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_cycle

    def create_appraisal_cycle(self, *, db: Session, appraisal_cycle: AppraisalCycleCreate) -> AppraisalCycleSchema:
        appraisal_cycle = appraisal_cycle_repo.create(db=db, obj_in=appraisal_cycle)
        return appraisal_cycle

    def update_appraisal_cycle(self, *, db: Session, id: UUID, appraisal_cycle: AppraisalCycleUpdate) -> AppraisalCycleSchema:
        appraisal_cycle_obj = appraisal_cycle_repo.get(db=db, id=id)
        if not appraisal_cycle_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_cycle not found")
        appraisal_cycle_ = appraisal_cycle_repo.update(db=db, db_obj=appraisal_cycle_obj, obj_in=appraisal_cycle)
        return appraisal_cycle_

    def get_appraisal_cycle(self, *, db: Session, id: UUID) -> AppraisalCycleSchema:
        appraisal_cycle = appraisal_cycle_repo.get(db=db, id=id)
        if not appraisal_cycle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_cycle not found")
        return appraisal_cycle

    def delete_appraisal_cycle(self, *, db: Session, id: UUID) -> AppraisalCycleSchema:
        appraisal_cycle = appraisal_cycle_repo.get(db=db, id=id)
        if not appraisal_cycle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_cycle not found")
        appraisal_cycle = appraisal_cycle_repo.remove(db=db, id=id)
        return appraisal_cycle

    def get_appraisal_cycle_by_id(self, *, id: UUID) -> AppraisalCycleSchema:
        appraisal_cycle = appraisal_cycle_repo.get(id)
        if not appraisal_cycle:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="appraisal_cycle not found"
            )
        return appraisal_cycle

    def iread(self, db: Session, value: str = None):
        search = "name"
        base = db.query(AppraisalCycle)
        response = []
       
        if search and value.strip():
            try:
                response = base.filter(
                    AppraisalCycle.__table__.c[search].ilike("%" + value.strip() + "%"))
              
                if not response.all():
                    response = base.filter(
                    AppraisalCycle.__table__.c["year"] == value.strip())
                
            except KeyError as ke:
                
                return ke.json()
        return response
    
    def read_appraisal_cycle_by_name_by_year(self, *, db:Session, search_word: str) -> List[AppraisalCycleSchema]:
        appraisal_cycle_name = self.iread(db=db, value=search_word)
        return appraisal_cycle_name
    



    def get_appraisal_cycle_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalCycleSchema]:
        pass

    def search_appraisal_cycle(self, *, db: Session, search: str, value: str) -> List[AppraisalCycleSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return appraisal_cycle_repo.get_by_kwargs(self, db, kwargs)


appraisal_cycle_service = AppraisalCycleService()