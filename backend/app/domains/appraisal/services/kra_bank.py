from typing import Any, List

from db.base_class import UUID
from domains.appraisal.respository.kra_bank import kra_bank_actions as kra_bank_repo
from domains.appraisal.models.department import Department
from domains.appraisal.models.kra_bank import KraBank
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.models.staff import Staff
from domains.appraisal.schemas.kra_bank import (
    KraBankCreate,
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
        self, *, db: Session, kra_bank: KraBankCreate
    ) -> KraBankSchema:
        
        # Validate department_id exists
        department = db.query(Department).filter(Department.id == kra_bank.department_id).first()
        if not department:
            raise ValueError("Department ID does not exist.")

        # Check for duplicate department_id in KraBank table
        duplicate_department = db.query(KraBank).filter(KraBank.department_id == kra_bank.department_id).first()
        if duplicate_department:
            raise ValueError("Duplicate Department ID in KraBank table.")

        # Validate appraisal_section_id exists
        appraisal_section = db.query(AppraisalSection).filter(AppraisalSection.id == kra_bank.appraisal_section_id).first()
        if not appraisal_section:
            raise ValueError("Appraisal Section ID does not exist.")

        # Validate supervisor_id exists
        supervisor = db.query(Staff).filter(Staff.id == kra_bank.supervisor_id).first()
        if not supervisor:
            raise ValueError("Supervisor ID does not exist.")

        # Create KRA Bank
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
