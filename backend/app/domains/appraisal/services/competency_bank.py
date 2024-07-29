from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.competency_bank import competency_bank_form_actions as competency_bank_form_repo
from domains.appraisal.schemas.competency_bank import CompentencyBankSchema, CompentencyBankCreate, CompentencyBankUpdate


class CompentencyBankService:


    def list_competency_bank_forms(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[ CompentencyBankSchema]:
        competency_bank_form = competency_bank_form_repo.get_all(db=db, skip=skip, limit=limit)
        return  competency_bank_form

    def create_competency_bank_forms(self, *, db: Session,  competency_bank_form: CompentencyBankCreate) ->  CompentencyBankSchema:
        competency_bank_form = competency_bank_form_repo.create(db=db, obj_in= competency_bank_form)
        return  competency_bank_form

    def update_competency_bank_forms(self, *, db: Session, id: UUID,  competency_bank_form:CompentencyBankUpdate) ->  CompentencyBankSchema:
        competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
        if not  competency_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" competency_bank_form not found")
        competency_bank_form = competency_bank_form_repo.update(db=db, db_obj= competency_bank_form, obj_in= competency_bank_form)
        return  competency_bank_form

    def get_competency_bank_forms(self, *, db: Session, id: UUID) ->  CompentencyBankSchema:
        competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
        if not  competency_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" competency_bank_form not found")
        return  competency_bank_form

    def delete_competency_bank_forms(self, *, db: Session, id: UUID) ->  CompentencyBankSchema:
        competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
        if not  competency_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" competency_bank_form not found")
        competency_bank_form = competency_bank_form_repo.remove(db=db, id=id)
        return  competency_bank_form

    def get_competency_bank_forms_by_id(self, *, id: UUID) ->  CompentencyBankSchema:
        competency_bank_form = competency_bank_form_repo.get(id)
        if not  competency_bank_form:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=" competency_bank_form not found"
            )
        return  competency_bank_form

    def get_competency_bank_forms_by_keywords(self, *, db: Session, tag: str) -> List[ CompentencyBankSchema]:
        pass

    def search_competency_banks_form(self, *, db: Session, search: str, value: str) -> List[ CompentencyBankSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return competency_bank_form_repo.get_by_kwargs(self, db, kwargs)


competency_bank_forms_service = CompentencyBankService