from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.staff import Staff_form_actions as Staff_form_repo
from domains.appraisal.schemas.staff import StaffSchema, StaffUpdate, StaffCreate
from domains.appraisal.models.staff import Staff
from domains.appraisal.models.department import Department


class StaffService:


    def list_staff(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffSchema]:
        staff = Staff_form_repo.get_all(db=db, skip=skip, limit=limit)
        return staff

    def create_staff(self, *, db: Session, staff: StaffCreate) -> StaffSchema:

         #check for duplicate email entries in staff table
        check_email = db.query(Staff).filter(Staff.email ==Staff.email).first()
        if check_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email already exist")


        #check if department_id exists in department table 
        check_department_id = db.query(Department).filter(Department.id ==Staff.department_id).first()
        if not check_department_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    
        staff = Staff_form_repo.create(db=db, obj_in=staff)
        return staff

    def update_staff(self, *, db: Session, id: UUID, staff: StaffUpdate) -> StaffSchema:
        staff_ = Staff_form_repo.get(db=db, id=id)
        if not staff_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        staff_ = Staff_form_repo.update(db=db, db_obj=staff, obj_in=staff)
        return staff_

    def get_staff(self, *, db: Session, id: UUID) -> StaffSchema:
        staff = Staff_form_repo.get(db=db, id=id)
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        return staff

    def delete_staff(self, *, db: Session, id: UUID) -> StaffSchema:
        staff = Staff_form_repo.get(db=db, id=id)
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        staff = Staff_form_repo.remove(db=db, id=id)
        return staff

    def get_staff_by_id(self, *, id: UUID) -> StaffSchema:
        staff = Staff_form_repo.get(id)
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="staff not found"
            )
        return staff

    def get_staff_by_keywords(self, *, db: Session, tag: str) -> List[StaffSchema]:
        pass

    def search_staff(self, *, db: Session, search: str, value: str) -> List[StaffSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return Staff_form_repo.get_by_kwargs(self, db, kwargs)


staff_service = StaffService()