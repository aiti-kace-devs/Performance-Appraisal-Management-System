from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.staff import Staff_form_actions as Staff_form_repo
from domains.appraisal.schemas.staff import StaffSchema, StaffUpdate, StaffCreate
from domains.appraisal.models.users import User
from domains.appraisal.models.roles import Role
from domains.appraisal.services.users import users_forms_service
class StaffService:


    def list_staff(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffSchema]:
        staff = Staff_form_repo.get_all(db=db, skip=skip, limit=limit)
        return staff

    def create_staff(self, *, db: Session, staff: StaffCreate) -> StaffSchema:

        check_if_role_id_exists = db.query(Role).filter(Role.id == staff.role_id).first()
        if not check_if_role_id_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role does not exist")


        staff_obj = Staff_form_repo.create(db=db, obj_in=staff)

        check_if_user_email_exists = db.query(User).filter(User.email == staff.email).first()
        if check_if_user_email_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="staff with email %s already exists" % staff.email)
        
        user_in = User()
        user_in.email = staff.email
        user_in.reset_password_token = None
        user_in.staff_id = staff_obj.id
        user_in.role_id = staff.role_id
        db.add(user_in)
        db.commit()
        db.refresh(user_in)

        return staff_obj

    def update_staff(self, *, db: Session, id: UUID, staff: StaffUpdate) -> StaffSchema:
        get_staff1 = Staff_form_repo.get(db=db, id=id)
        if not get_staff1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        update_staff = Staff_form_repo.update(db=db, db_obj=get_staff1, obj_in=staff)
        return update_staff

    def get_staff(self, *, db: Session, id: UUID) -> StaffSchema:
        get_staff = Staff_form_repo.get(db=db, id=id)
        if not get_staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        return get_staff

    def delete_staff(self, *, db: Session, id: UUID) -> StaffSchema:
        get_staff2 = Staff_form_repo.get(db=db, id=id)
        if not get_staff2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        delete_staff = Staff_form_repo.remove(db=db, id=id)
        return delete_staff

    def get_staff_by_id(self, *, id: UUID) -> StaffSchema:
        get_staff_by_id = Staff_form_repo.get(id)
        if not get_staff_by_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="staff not found"
            )
        return get_staff_by_id

    def get_staff_by_keywords(self, *, db: Session, tag: str) -> List[StaffSchema]:
        pass

    def search_staff(self, *, db: Session, search: str, value: str) -> List[StaffSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return Staff_form_repo.get_by_kwargs(self, db, kwargs)


staff_service = StaffService()