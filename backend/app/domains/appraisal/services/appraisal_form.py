from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.base_class import UUID
from domains.appraisal.respository.appraisal_form import Appraisal_form_actions as Appraisal_form_repo
from domains.appraisal.schemas.appraisal_form import AppraisalFormSchema, AppraisalFormUpdate, AppraisalFormCreate
from domains.appraisal.models.appraisal_form import AppraisalForm
from domains.appraisal.models.appraisal_section import AppraisalSection
from fastapi.encoders import jsonable_encoder
import json


class AppraisalFormService:


    def list_appraisal_form(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalFormSchema]:
        appraisal_form = Appraisal_form_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_form
    




    def create_appraisal_form(self, db: Session, payload: AppraisalFormCreate,  **kw):
        
        #check if the appraisal section ID exists in the appraisal section table
        check_appraisal_section_id = db.query(AppraisalSection).filter(AppraisalSection.id ==payload.appraisal_sections_id).first()
        if not check_appraisal_section_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal Section ID not found")


        obj_in_data = jsonable_encoder(payload, **kw)
        json_data = jsonable_encoder({key: item for key, item in enumerate(payload.form_fields)})

        new_appraisal_form = AppraisalForm(**obj_in_data)
        new_appraisal_form.form_fields = json.dumps(json_data)
        new_appraisal_form.appraisal_sections_id = payload.appraisal_sections_id
        new_appraisal_form.created_by = None
        db.add(new_appraisal_form)
        db.commit()
        db.refresh(new_appraisal_form)

        form_fields = json.loads(new_appraisal_form.form_fields)

        return {
                "id": new_appraisal_form.id,
                "created_by": new_appraisal_form.created_by,
                "appraisal_sections": {
                    "id": new_appraisal_form.appraisal_sections.id,
                    "name": new_appraisal_form.appraisal_sections.name,
                    "description": new_appraisal_form.appraisal_sections.description,
                    "appraisal_year": new_appraisal_form.appraisal_sections.appraisal_year
                },
                "form_fields": [form_fields]
            }
    



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
    
    

    def get_appraisal_form_by_id(self, db: Session, id: UUID) -> AppraisalFormSchema:
        
        data = db.query(AppraisalForm).filter(AppraisalForm.id == id).first()
        if not data:
            data = []
            return {
            "data": data
            }
        
        form_fields = json.loads(data.form_fields)

        return {
                "id": data.id,
                "created_by": data.created_by,
                "appraisal_sections": {
                    "id": data.appraisal_sections.id,
                    "name": data.appraisal_sections.name,
                    "description": data.appraisal_sections.description,
                    "appraisal_year": data.appraisal_sections.appraisal_year
                },
                "form_fields": [form_fields]
            }




    def get_appraisal_form_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalFormSchema]:
        pass

    def search_appraisal_form(self, *, db: Session, search: str, value: str) -> List[AppraisalFormSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return Appraisal_form_repo.get_by_kwargs(self, db, kwargs)


appraisal_form_service = AppraisalFormService()