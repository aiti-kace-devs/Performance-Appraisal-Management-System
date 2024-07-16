from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from backend.app.domains.appraisal.respository.appraisal import appraisal_form_actions as appraisal_form_repo
from backend.app.domains.appraisal.schemas.appraisal import AppraisalFormSchema, AppraisalFormUpdate, AppraisalFormCreate


class AppraisalFormService:


    def list_appraisal_form(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalFormSchema]:
        appraisal_form = appraisal_form_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_form

    def create_appraisal_form(self, *, db: Session, appraisal_form: AppraisalFormCreate) -> AppraisalFormSchema:
        appraisal_form = appraisal_form_repo.create(db=db, obj_in=appraisal_form)
        return appraisal_form

    def update_appraisal_form(self, *, db: Session, id: UUID, appraisal_form: AppraisalFormUpdate) -> AppraisalFormSchema:
        appraisal_form = appraisal_form_repo.get(db=db, id=id)
        if not appraisal_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_form not found")
        appraisal_form = appraisal_form_repo.update(db=db, db_obj=appraisal_form, obj_in=appraisal_form)
        return appraisal_form

    def get_appraisal_form(self, *, db: Session, id: UUID) -> AppraisalFormSchema:
        appraisal_form = appraisal_form_repo.get(db=db, id=id)
        if not appraisal_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_form not found")
        return appraisal_form

    def delete_appraisal_form(self, *, db: Session, id: UUID) -> AppraisalFormSchema:
        appraisal_form = appraisal_form_repo.get(db=db, id=id)
        if not appraisal_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_form not found")
        appraisal_form = appraisal_form_repo.remove(db=db, id=id)
        return appraisal_form

    def get_appraisal_form_by_id(self, *, id: UUID) -> AppraisalFormSchema:
        appraisal_form = appraisal_form_repo.get(id)
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
        return appraisal_form_repo.get_by_kwargs(self, db, kwargs)


appraisal_form_service = AppraisalFormService()