from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from domains.appraisal.schemas.staff import StaffSchema, StaffWithFullNameInDBBase,DepartmentInfo,RoleInfo
from db.base_class import UUID
from domains.appraisal.respository.department import department_actions as department_repo
from domains.appraisal.models.department import Department
from domains.appraisal.schemas.department import DepartmentSchema, DepartmentUpdate, DepartmentCreate, DepartmentWithTotalStaff
from domains.appraisal.models.staff import Staff
from sqlalchemy import func
from domains.appraisal.models.role_permissions import Role
from domains.auth.models.users import User
from fastapi.encoders import jsonable_encoder

class AppraisalService:


    def list_department(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[DepartmentWithTotalStaff]:
        # Fetch departments with the count of staff
        departments = (
            db.query(
                Department,
                func.count(Staff.id).label('staff_count')  # Count staff members
            )
            .select_from(Department)  # Start from Department
            .outerjoin(Staff, Department.id == Staff.department_id)  # Use explicit ON clause for joining
            .group_by(Department.id)  # Group by department ID
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Map the results to the desired schema
        department_list = [
            DepartmentWithTotalStaff(
                id=dept.id,
                name=dept.name,
                description=dept.description,
                total_staff=staff_count  # Include the staff count
            )
            for dept, staff_count in departments
        ]

        return department_list


    def create_department(self, *, db: Session, department: DepartmentCreate) -> DepartmentWithTotalStaff:
        # Check if the department name already exists
        check_department_name = db.query(Department).filter(Department.name == department.name).first()
        if check_department_name:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department name already exists")

        # Create a new department
        new_department = jsonable_encoder(department)
        db_obj = Department(**new_department)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


        department_list = {
                'id':db_obj.id,
                'name':db_obj.name,
                'description':db_obj.description,
                'total_staff': 0
        }

        return department_list



    


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
    


    

    def list_all_staff_under_department(self, *, db: Session, id: UUID, skip: int = 0, limit: int = 100) -> List[StaffWithFullNameInDBBase]: 
        staff_query = (
            db.query(Staff, 
                    Department.id.label('department_id'), 
                    Department.name.label('department_name'), 
                    Role.id.label('role_id'), 
                    Role.name.label('role_name'))
            .join(Department, Staff.department_id == Department.id)
            .join(User, User.staff_id == Staff.id)
            .join(Role, User.role_id == Role.id)
            .filter(Staff.department_id == id)
            .offset(skip)
            .limit(limit)
        )
        
        staff_with_details = staff_query.all()
        
        staff_list = [
            StaffWithFullNameInDBBase(
                id=staff.id,
                title=staff.title,
                first_name=staff.first_name,
                last_name=staff.last_name,
                other_name=staff.other_name,
                full_name=f"{staff.first_name} {staff.last_name}" + (f" {staff.other_name}" if staff.other_name else ""),
                gender=staff.gender,
                email=staff.email,
                position=staff.position,
                grade=staff.grade,
                appointment_date=staff.appointment_date,
                department_id=DepartmentInfo(
                    id=department_id,
                    name=department_name
                ),
                role_id=RoleInfo(
                    id=role_id,
                    name=role_name
                )
            )
            for staff, department_id, department_name, role_id, role_name in staff_with_details
        ]
        
        return staff_list

    

    def check_if_department_has_staff(self,db: Session, id: UUID):

        get_department = db.query(Staff).filter(Staff.department_id == id).all()
        
        if get_department:
            return True

        return False



department_service = AppraisalService()