from typing import Any, List

from db.base_class import UUID
from domains.appraisal.respository.kra_bank import kra_bank_actions as kra_bank_repo
from domains.appraisal.schemas.kra_bank import (
    KraBankBaseCreate,
    KraBankSchema,
    KraBankUpdate,
)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class KraBankService:
    def list_kra_bank(
        self, *, db: Session, skip: int = 0, limit: int = 100
    ) -> List[KraBankSchema]:
        kra_bank = kra_bank_repo.get_all(db=db, skip=skip, limit=limit)
        return kra_bank

    def create_kra_bank(
        self, *, db: Session, kra_bank: KraBankBaseCreate
    ) -> KraBankSchema:
        kra_bank = kra_bank_repo.create(db=db, obj_in=kra_bank)
        return kra_bank

    def update_kra_bank(
        self, *, db: Session, id: UUID, kra_bank: KraBankUpdate
    ) -> KraBankSchema:
        kra_bank = kra_bank_repo.get(db=db, id=id)
        if not kra_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="kra bank not found"
            )
        kra_bank = kra_bank_repo.update(db=db, db_obj=kra_bank, obj_in=kra_bank)
        return kra_bank

    def get_kra_bank(self, *, db: Session, id: UUID) -> KraBankSchema:
        kra_bank = kra_bank_repo.get(db=db, id=id)
        if not kra_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="kra Bank not found"
            )
        return kra_bank

    def delete_kra_bank(self, *, db: Session, id: UUID) -> KraBankSchema:
        kra_bank = kra_bank_repo.get(db=db, id=id)
        if not kra_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="kra_bank not found"
            )
        kra_bank = kra_bank_repo.remove(db=db, id=id)
        return kra_bank

    def get_kra_bank_by_id(self, *, id: UUID) -> KraBankSchema:
        kra_bank = kra_bank_repo.get(id)
        if not kra_bank:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="kra_bank not found"
            )
        return kra_bank

    def get_kra_bank_by_keywords(self, *, db: Session, tag: str) -> List[KraBankSchema]:
        pass

    def search_kra_bank(
        self, *, db: Session, search: str, value: str
    ) -> List[KraBankSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return kra_bank_repo.get_by_kwargs(self, db, kwargs)


kra_bank_service = KraBankService()
