from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.staff_deadline import staff_deadline_actions as staff_deadline_repo
from domains.appraisal.schemas.staff_deadline import StaffDeadlineSchema, StaffDeadlineUpdate, StaffDeadlineCreate
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.models.staff import Staff

class StaffDeadlineService:


    def list_staff_deadline(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffDeadlineSchema]:
        list_staff_deadline = staff_deadline_repo.get_all(db=db, skip=skip, limit=limit)
        return list_staff_deadline

    def create_staff_deadline(self, *, db: Session, staff_deadline: StaffDeadlineCreate) -> StaffDeadlineSchema:

        check_appraisal_section = db.query(AppraisalSection).filter(AppraisalSection.id == staff_deadline.appraisal_sections_id).first()
        if not check_appraisal_section:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="appraisal section not found")
        
        check_staff_id = db.query(Staff).filter(Staff.id == staff_deadline.staffs_id).first()
        if not check_staff_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="staff with id %s not found in staff table" % staff_deadline.staffs_id)
        
        check_supervisor_id = db.query(Staff).filter(Staff.id == staff_deadline.supervisor_id).first()
        if not check_supervisor_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="supervisor with id %s not found in staff table" % staff_deadline.supervisor_id)
        
        create_staff_deadline = staff_deadline_repo.create(db=db, obj_in=staff_deadline)
        return create_staff_deadline

    def update_staff_deadline(self, *, db: Session, id: UUID, staff_deadline: StaffDeadlineUpdate) -> StaffDeadlineSchema:
        get_staff_deadline = staff_deadline_repo.get(db=db, id=id)
        if not get_staff_deadline:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff deadline not found")
        update_staff_deadline = staff_deadline_repo.update(db=db, db_obj=get_staff_deadline, obj_in=staff_deadline)
        return update_staff_deadline

    def get_staff_deadline_by_id(self, *, db: Session, id: UUID) -> StaffDeadlineSchema:
        get = staff_deadline_repo.get(db=db, id=id)
        if not get:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff deadline not found")
        return get

    def delete_staff_deadline(self, *, db: Session, id: UUID) -> StaffDeadlineSchema:
        get2 = staff_deadline_repo.get(db=db, id=id)
        if not get2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff deadline not found")
        delete_staff_deadline = staff_deadline_repo.remove(db=db, id=id)
        return delete_staff_deadline

    # def get_staff_deadline_by_id(self, *, id: UUID) -> StaffDeadlineSchema:
    #     staff_deadline = staff_deadline_repo.get(id)
    #     if not staff_deadline:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="staff_deadline not found"
    #         )
    #     return staff_deadline

    def get_staff_deadline_by_keywords(self, *, db: Session, tag: str) -> List[StaffDeadlineSchema]:
        pass

    def search_staff_deadline(self, *, db: Session, search: str, value: str) -> List[StaffDeadlineSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return staff_deadline_repo.get_by_kwargs(self, db, kwargs)


staff_deadline_service = StaffDeadlineService()