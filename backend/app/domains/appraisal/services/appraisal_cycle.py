from typing import List, Any,Annotated
import re
from fastapi import HTTPException, status,Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.base_class import UUID
from domains.appraisal.respository.appraisal_cycle import appraisal_cycle_actions as appraisal_cycle_repo
from domains.appraisal.schemas.appraisal_cycle import AppraisalCycleSchema, AppraisalCycleUpdate, AppraisalCycleCreate,ReadAppraisalSectionWithCycleBase
from domains.appraisal.models.appraisal_cycle import AppraisalCycle
from domains.appraisal.models.staff_role_permissions import Staff
from datetime import datetime
from utils.rbac import get_current_user
from domains.auth.models.users import User
from utils import rbac
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.schemas import appraisal_section


class AppraisalCycleService:


    def list_appraisal_cycle(self, *, current_user: Annotated[User, Depends(rbac.get_current_user)], db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalCycleSchema]:
        appraisal_cycle = db.query(AppraisalCycle).filter(AppraisalCycle.created_by == current_user.staff_id).all()
        if not appraisal_cycle:
            return []
        return appraisal_cycle
    




    def create_appraisal_cycle(self, *, db: Session, 
                               payload: AppraisalCycleCreate,
                                 current_user: Annotated[User, Depends(rbac.get_current_user)]
                                 ) -> AppraisalCycleSchema:

        date = datetime.now()
        current_year = date.year


        check_if_staff_exist = db.query(Staff).filter(Staff.id == current_user.staff_id).first()
        if not check_if_staff_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff does not exist")
        

        check_for_duplicate = db.query(AppraisalCycle).filter(AppraisalCycle.name == payload.name, AppraisalCycle.year == current_year, AppraisalCycle.created_by == current_user.staff_id).first()

        if check_for_duplicate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal Cycle %s already exists for this year" % payload.name)

        
        
        create_appraisal_cycl = AppraisalCycle()
        create_appraisal_cycl.name = payload.name
        create_appraisal_cycl.description = payload.description
        create_appraisal_cycl.year = current_year
        create_appraisal_cycl.created_by = current_user.staff_id
        db.add(create_appraisal_cycl)
        db.commit()
        db.refresh(create_appraisal_cycl)
        return create_appraisal_cycl
    






    def get_appraisal_sections_under_appraisal_cycle(self, *, db: Session, id: UUID, current_user: Annotated[User, Depends(rbac.get_current_user)]) -> ReadAppraisalSectionWithCycleBase:
        get_appraisal_cycle = appraisal_cycle_repo.get(db=db, id=id)

        get_appraisal_sections = []
        if not get_appraisal_cycle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal Cycle not found")
        
        get_appraisal_sections = db.query(AppraisalSection).filter(AppraisalSection.created_by == current_user.staff_id, AppraisalSection.appraisal_cycle_id == id).all()

        if not get_appraisal_sections:
            get_appraisal_sections = []
        
        appraisal_sections = get_appraisal_sections
        return {
            "id": get_appraisal_cycle.id,
            "name": get_appraisal_cycle.name,
            "description": get_appraisal_cycle.description,
            "year": get_appraisal_cycle.year,
            "created_by": get_appraisal_cycle.created_by,
            "created_date": get_appraisal_cycle.created_date,
            "updated_date": get_appraisal_cycle.updated_date,
            "appraisal_sections": appraisal_sections
        }








    def update_appraisal_cycle(self, *, db: Session, id: UUID, appraisal_cycle: AppraisalCycleUpdate) -> AppraisalCycleSchema:
        appraisal_cycle_obj = appraisal_cycle_repo.get(db=db, id=id)
        if not appraisal_cycle_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_cycle not found")
        appraisal_cycle_ = appraisal_cycle_repo.update(db=db, db_obj=appraisal_cycle_obj, obj_in=appraisal_cycle)
        return appraisal_cycle_
    






    def delete_appraisal_cycle(self, *, db: Session, id: UUID, current_user: Annotated[User, Depends(rbac.get_current_user)]) -> AppraisalCycleSchema:
        appraisal_cycle = appraisal_cycle_repo.get(db=db, id=id)
        if not appraisal_cycle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal Cycle not found")
        get_appraisal_sections = db.query(AppraisalSection).filter(AppraisalSection.appraisal_cycle_id == id).all()
        if get_appraisal_sections:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This Appraisal Cycle has sections so it can not be deleted")
        appraisal_cycle = appraisal_cycle_repo.remove(db=db, id=id)
        return appraisal_cycle








    def get_appraisal_cycle(self, *, db: Session, id: UUID) -> AppraisalCycleSchema:
        appraisal_cycle = appraisal_cycle_repo.get(db=db, id=id)
        if not appraisal_cycle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_cycle not found")
        return appraisal_cycle



    def get_appraisal_cycle_by_id(self, *, id: UUID) -> AppraisalCycleSchema:
        appraisal_cycle = appraisal_cycle_repo.get(id)
        if not appraisal_cycle:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="appraisal_cycle not found"
            )
        return appraisal_cycle
    
    # Check if value is an integer and formatted as yyyy
    def is_valid_year(self, year_str: str) -> bool:
        return year_str.isdigit() and len(year_str) == 4
    

    def iread(self, db: Session, value: str) -> List[AppraisalCycle]:
        search_field = "name"
        response = []

        # Sanitize and validate input
        search_value = re.sub(r'[^\w\s]', '', value.strip())  # Remove special characters
        if not search_value:
            return response

        try:
            # Use parameterized queries to prevent SQL injection
            if search_field and search_value:
                response = db.query(AppraisalCycle).filter(
                    getattr(AppraisalCycle, search_field).ilike(f"%{search_value}%")
                ).all()

                if not response and self.is_valid_year(value.strip()):
                    response = db.query(AppraisalCycle).filter(
                        AppraisalCycle.year == search_value
                    ).all()

        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            # Log the error and return a safe message
            # log.error(f"Database error occurred: {e}")
            return {"error": "An error occurred while processing your request."}
        except KeyError as ke:
            # Log the error and return a safe message
            # log.error(f"Key error: {ke}")
            print(f"Key error: {ke}")
            return {"error": "Invalid search parameter."}

        return response
    

    
    def search_cycle_by_year(self, db: Session, value: int) -> List[AppraisalCycle]:
        # search_field = "name"
        response = []

        # Sanitize and validate input
        # search_value = re.sub(r'[^\w\s]', '', value.strip())  # Remove special characters
        # if not search_value:
        #     return response

        try:
            # Use parameterized queries to prevent SQL injection
            # if search_field and search_value:
            #     response = db.query(AppraisalCycle).filter(
            #         getattr(AppraisalCycle, search_field).ilike(f"%{search_value}%")
            #     ).all()

            if not response and self.is_valid_year(value):
                response = db.query(AppraisalCycle).filter(
                    AppraisalCycle.year == value
                ).all()

        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            # Log the error and return a safe message
            # log.error(f"Database error occurred: {e}")
            return {"error": "An error occurred while processing your request."}
        except KeyError as ke:
            # Log the error and return a safe message
            # log.error(f"Key error: {ke}")
            print(f"Key error: {ke}")
            return {"error": "Invalid search parameter."}

        return response
    
    def read_appraisal_cycle_by_name_by_year(self, *, db:Session, search_word: str) -> List[AppraisalCycleSchema]:
        appraisal_cycle_name = self.iread(db=db, value=search_word)
        return appraisal_cycle_name
    



    def get_appraisal_cycle_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalCycleSchema]:
        pass

    def search_appraisal_cycle(self, *, db: Session, search: str, value: str) -> List[AppraisalCycleSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return appraisal_cycle_repo.get_by_kwargs(self, db, kwargs)


appraisal_cycle_service = AppraisalCycleService()