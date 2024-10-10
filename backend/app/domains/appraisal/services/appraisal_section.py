from typing import List, Any
import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.base_class import UUID
from domains.appraisal.respository.appraisal_section import appraisal_section_actions as appraisal_section_repo
from domains.appraisal.schemas.appraisal_section import AppraisalSectionSchema, AppraisalSectionUpdate, AppraisalSectionCreate
from domains.appraisal.models.appraisal_section import AppraisalSection
from datetime import datetime
from domains.appraisal.models.appraisal_cycle import AppraisalCycle


class AppraisalSectionService:


    def list_appraisal_section(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalSectionSchema]:
        appraisal_section = appraisal_section_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_section
    

    def create_appraisal_section(self, *, db: Session, payload: AppraisalSectionCreate) -> AppraisalSectionSchema:

        date = datetime.now()
        current_year = date.year

        appraisal_cycle_data = None

        check_for_duplicate = db.query(AppraisalSection).filter(AppraisalSection.name == payload.name, AppraisalSection.appraisal_year == current_year).first()

        if check_for_duplicate:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Appraisal Section {payload.name} already exists for {current_year}"
                )

        
        get_appraisal_cycle = db.query(AppraisalCycle).filter(AppraisalCycle.year == current_year).first()
        if not get_appraisal_cycle:
            appraisal_cycle_data = None


        appraisal_cycle_data = get_appraisal_cycle.id
            
        create_section = AppraisalSection()
        create_section.name = payload.name
        create_section.description = payload.description
        create_section.appraisal_year = current_year
        create_section.appraisal_cycle_id = appraisal_cycle_data
        create_section.created_by = None
        db.add(create_section)
        db.commit()
        db.refresh(create_section)

        

        return {
            "id": create_section.id,
            "name": create_section.name,
            "description": create_section.description,
            "appraisal_year": create_section.appraisal_year,
            "created_by": create_section.created_by,
            "appraisal_cycle": {
                "id": create_section.appraisal_cycles.id,
                "name": create_section.appraisal_cycles.name
            },
            "created_at": create_section.created_date,
            "updated_at": create_section.updated_date
        }

    


    def update_appraisal_section(self, *, db: Session, id: UUID, appraisal_section: AppraisalSectionUpdate) -> AppraisalSectionSchema:
        appraisal_section_obj = appraisal_section_repo.get(db=db, id=id)
        if not appraisal_section_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_section not found")
        appraisal_section_ = appraisal_section_repo.update(db=db, db_obj=appraisal_section_obj, obj_in=appraisal_section)
        return appraisal_section_

    def get_appraisal_section(self, *, db: Session, id: UUID) -> AppraisalSectionSchema:
        appraisal_section = appraisal_section_repo.get(db=db, id=id)
        if not appraisal_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_section not found")
        return appraisal_section

    def delete_appraisal_section(self, *, db: Session, id: UUID) -> AppraisalSectionSchema:
        appraisal_section = appraisal_section_repo.get(db=db, id=id)
        if not appraisal_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_section not found")
        appraisal_section = appraisal_section_repo.remove(db=db, id=id)
        return appraisal_section

    def get_appraisal_section_by_id(self, *, id: UUID) -> AppraisalSectionSchema:
        appraisal_section = appraisal_section_repo.get(id)
        if not appraisal_section:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="appraisal_section not found"
            )
        return appraisal_section
    
    # # Check if value is an integer and formatted as yyyy
    # def is_valid_year(self, year_str: str) -> bool:
    #     return year_str.isdigit() and len(year_str) == 4
    

    # def iread(self, db: Session, value: str) -> List[AppraisalSection]:
    #     search_field = "name"
    #     response = []

    #     # Sanitize and validate input
    #     search_value = re.sub(r'[^\w\s]', '', value.strip())  # Remove special characters
    #     if not search_value:
    #         return response

    #     try:
    #         # Use parameterized queries to prevent SQL injection
    #         if search_field and search_value:
    #             response = db.query(AppraisalSection).filter(
    #                 getattr(AppraisalSection, search_field).ilike(f"%{search_value}%")
    #             ).all()

    #             if not response and self.is_valid_year(value.strip()):
    #                 response = db.query(AppraisalSection).filter(
    #                     AppraisalSection.year == search_value
    #                 ).all()

    #     except SQLAlchemyError as e:
    #         print(f"Database error occurred: {e}")
    #         # Log the error and return a safe message
    #         # log.error(f"Database error occurred: {e}")
    #         return {"error": "An error occurred while processing your request."}
    #     except KeyError as ke:
    #         # Log the error and return a safe message
    #         # log.error(f"Key error: {ke}")
    #         print(f"Key error: {ke}")
    #         return {"error": "Invalid search parameter."}

    #     return response
    
    # def read_appraisal_section_by_name_by_year(self, *, db:Session, search_word: str) -> List[AppraisalSectionSchema]:
    #     appraisal_section_name = self.iread(db=db, value=search_word)
    #     return appraisal_section_name
    



    def get_appraisal_section_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalSectionSchema]:
        pass

    def search_appraisal_section(self, *, db: Session, search: str, value: str) -> List[AppraisalSectionSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return appraisal_section_repo.get_by_kwargs(self, db, kwargs)


appraisal_section_service = AppraisalSectionService()