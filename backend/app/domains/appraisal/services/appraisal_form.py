from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.base_class import UUID
from domains.appraisal.respository.appraisal_form import Appraisal_form_actions as Appraisal_form_repo
from domains.appraisal.schemas.appraisal_form import AppraisalFormSchema, AppraisalFormUpdate, AppraisalFormCreate
from domains.appraisal.models.appraisal import Appraisal
from domains.appraisal.models.appraisal_section import AppraisalSection


class AppraisalFormService:


    def list_appraisal_form(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalFormSchema]:
        appraisal_form = Appraisal_form_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_form

    def create_appraisal_form(self, *, db: Session, appraisal_form: AppraisalFormCreate) -> AppraisalFormSchema:

        #check if the appraisal ID exists in the appraisal table
        check_appraisal_id = db.query(Appraisal).filter(Appraisal.id ==appraisal_form.appraisal_id).first()
        if not check_appraisal_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal ID not found")
        
        #check if the appraisal section ID exists in the appraisal section table
        check_appraisal_section_id = db.query(AppraisalSection).filter(AppraisalSection.id ==appraisal_form.appraisal_sections_id).first()
        if not check_appraisal_section_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal ID not found")


        appraisal_form = Appraisal_form_repo.create(db=db, obj_in=appraisal_form)
        return appraisal_form

    def update_appraisal_form(self, *, db: Session, id: UUID, appraisal_form: AppraisalFormUpdate) -> AppraisalFormSchema:
        appraisal_form_ = Appraisal_form_repo.get(db=db, id=id)
        if not appraisal_form_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_form not found")
        appraisal_form_ = Appraisal_form_repo.update(db=db, db_obj=appraisal_form_, obj_in=appraisal_form)
        return appraisal_form_

    def get_appraisal_form(self, *, db: Session, id: UUID) -> AppraisalFormSchema:
        appraisal_form = Appraisal_form_repo.get(db=db, id=id)
        if not appraisal_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_form not found")
        return appraisal_form

    def delete_appraisal_form(self, *, db: Session, id: UUID) -> AppraisalFormSchema:
        appraisal_form = Appraisal_form_repo.get(db=db, id=id)
        if not appraisal_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_form not found")
        appraisal_form = Appraisal_form_repo.remove(db=db, id=id)
        return appraisal_form

    def get_appraisal_form_by_id(self, *, id: UUID) -> AppraisalFormSchema:
        appraisal_form = Appraisal_form_repo.get(id)
        if not appraisal_form:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="appraisal_form not found"
            )
        return appraisal_form

    def get_appraisal_form_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalFormSchema]:
        pass

    def search_appraisal_form(self, *, db: Session, search: str, value: str) -> List[AppraisalFormSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return Appraisal_form_repo.get_by_kwargs(self, db, kwargs)


appraisal_form_service = AppraisalFormService()