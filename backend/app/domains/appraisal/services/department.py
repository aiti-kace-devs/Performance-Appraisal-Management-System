from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from domains.appraisal.schemas.staff import StaffSchema
from db.base_class import UUID
from domains.appraisal.respository.department import department_actions as department_repo
from domains.appraisal.models.department import Department
from domains.appraisal.schemas.department import DepartmentSchema, DepartmentUpdate, DepartmentCreate
from domains.appraisal.models.staff_role_permissions import Staff

class AppraisalService:


    def list_department(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[DepartmentSchema]:
        department = department_repo.get_all(db=db, skip=skip, limit=limit)
        return department

    def create_department(self, *, db: Session, department: DepartmentCreate) -> DepartmentSchema:
        check_department_name = db.query(Department).filter(Department.name == department.name).first()
        if check_department_name:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department name already exist")
        department = department_repo.create(db=db, obj_in=department)
        return department

    def update_department(self, *, db: Session, id: UUID, department: DepartmentUpdate) -> DepartmentSchema:
        department_ = department_repo.get(db=db, id=id)
        if not department_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="department not found")
        department = department_repo.update(db=db, db_obj=department_, obj_in=department)
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
    

    def list_all_staff_under_department(self, *, db: Session, id: UUID, skip: int = 0, limit: int = 100)  -> List[StaffSchema]:
        staff_query = db.query(Staff, Department.name).filter(Staff.department_id == id).join(Department, Staff.department_id == Department.id).offset(skip).limit(limit)
        
        # Fetch results
        staff_with_department = staff_query.all()
        
        # Create StaffSchema instances
        staff_list = [StaffSchema(
            id=staff.id, title=staff.title, first_name=staff.first_name, last_name=staff.last_name,
            other_name=staff.other_name, gender=staff.gender,
            email=staff.email, position=staff.position,
            grade=staff.grade, appointment_date=staff. appointment_date,
            department_id=department_name
            ) for staff, department_name in staff_with_department]
        
        return staff_list



department_service = AppraisalService()