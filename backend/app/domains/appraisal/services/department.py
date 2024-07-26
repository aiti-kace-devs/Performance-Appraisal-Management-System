from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.department import department_actions as department_repo
from domains.appraisal.schemas.department import DepartmentSchema, DepartmentUpdate, DepartmentCreate


class AppraisalService:


    def list_department(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[DepartmentSchema]:
        department = department_repo.get_all(db=db, skip=skip, limit=limit)
        return department

    def create_department(self, *, db: Session, department: DepartmentCreate) -> DepartmentSchema:
        department = department_repo.create(db=db, obj_in=department)
        return department

    def update_department(self, *, db: Session, id: UUID, department: DepartmentUpdate) -> DepartmentSchema:
        department = department_repo.get(db=db, id=id)
        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="department not found")
        department = department_repo.update(db=db, db_obj=department, obj_in=department)
        return department

    def get_department(self, *, db: Session, id: UUID) -> DepartmentSchema:
        department = department_repo.get(db=db, id=id)
        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="department not found")
        return department

    def delete_department(self, *, db: Session, id: UUID) -> DepartmentSchema:
        department = department_repo.get(db=db, id=id)
        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="department not found")
        department = department_repo.remove(db=db, id=id)
        return department

    def get_department_by_id(self, *, id: UUID) -> DepartmentSchema:
        department = department_repo.get(id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="department not found"
            )
        return department

    def get_department_by_keywords(self, *, db: Session, tag: str) -> List[DepartmentSchema]:
        pass

    def search_department(self, *, db: Session, search: str, value: str) -> List[DepartmentSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return department_repo.get_by_kwargs(self, db, kwargs)


department_service = AppraisalService()