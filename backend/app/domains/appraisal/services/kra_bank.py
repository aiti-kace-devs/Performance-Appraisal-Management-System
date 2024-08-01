from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.kra_bank import kra_bank_form_actions as kra_bank_form_repo
from domains.appraisal.schemas.kra_bank import KraBankSchema, KraBankUpdate, KraBankCreate


class KraBankService:


    def list_kra_bank_form(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[KraBankSchema]:
        kra_bank_form = kra_bank_form_repo.get_all(db=db, skip=skip, limit=limit)
        return kra_bank_form

    def create_kra_bank_form(self, *, db: Session, kra_bank_form: KraBankCreate) -> KraBankSchema:
        kra_bank_form = kra_bank_form_repo.create(db=db, obj_in=kra_bank_form)
        return kra_bank_form

    def update_kra_bank_form(self, *, db: Session, id: UUID, kra_bank_form: KraBankUpdate) -> KraBankSchema:
        kra_bank_form = kra_bank_form_repo.get(db=db, id=id)
        if not kra_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="kra_bank_form not found")
        kra_bank_form = kra_bank_form_repo.update(db=db, db_obj=kra_bank_form, obj_in=kra_bank_form)
        return kra_bank_form

    def get_kra_bank_form(self, *, db: Session, id: UUID) -> KraBankSchema:
        kra_bank_form = kra_bank_form_repo.get(db=db, id=id)
        if not kra_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="kra_bank_form not found")
        return kra_bank_form

    def delete_kra_bank_form(self, *, db: Session, id: UUID) -> KraBankSchema:
        kra_bank_form = kra_bank_form_repo.get(db=db, id=id)
        if not kra_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="kra_bank_form not found")
        kra_bank_form = kra_bank_form_repo.remove(db=db, id=id)
        return kra_bank_form

    def get_kra_bank_form_by_id(self, *, id: UUID) -> KraBankSchema:
        kra_bank_form = kra_bank_form_repo.get(id)
        if not kra_bank_form:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="kra_bank_form not found"
            )
        return kra_bank_form

    def get_kra_bank_form_by_keywords(self, *, db: Session, tag: str) -> List[KraBankSchema]:
        pass

    def search_kra_bank_form(self, *, db: Session, search: str, value: str) -> List[KraBankSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return kra_bank_form_repo.get_by_kwargs(self, db, kwargs)


kra_bank_form_service = KraBankService()