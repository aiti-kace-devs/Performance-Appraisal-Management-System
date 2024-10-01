from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.competency_bank import competency_bank_form_actions as competency_bank_form_repo
from domains.appraisal.schemas.competency_bank import CompetencyBankSchema, CompetencyBankUpdate, CompetencyBankCreate
from domains.appraisal.models.staff_role_permissions import Staff
from domains.appraisal.models.competency_bank import CompetencyBank
from domains.appraisal.models.appraisal_section import AppraisalSection


class CompetencyBankService:


    def list_competency_bank_form(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[CompetencyBankSchema]:
        competency_bank_form = competency_bank_form_repo.get_all(db=db, skip=skip, limit=limit)
        return competency_bank_form

    def create_competency_bank_form(self, *, db: Session, competency_bank_form: CompetencyBankCreate) -> CompetencyBankSchema:


         #checking if appraisal section_id is already in compentency_bank table 
        check_section_id = db.query(CompetencyBank).filter(CompetencyBank.appraisal_section_id ==competency_bank_form.appraisal_section_id).first()
        if check_section_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal section already exist")
        
        #check if appraisal section_id is already in appraisal section table 
        check_appraisal_section_id = db.query(AppraisalSection).filter(AppraisalSection.id ==competency_bank_form.appraisal_section_id).first()
        if not check_appraisal_section_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appraisal section not found")
        

        #check if staff_id is already in staff table 
        check_staff_id = db.query(Staff).filter(Staff.id ==competency_bank_form.staff_id).first()
        if not check_staff_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")











        competency_bank_form = competency_bank_form_repo.create(db=db, obj_in=competency_bank_form)
        return competency_bank_form

    def update_competency_bank_form(self, *, db: Session, id: UUID, competency_bank_form: CompetencyBankUpdate) -> CompetencyBankSchema:
        competency_bank_form_ = competency_bank_form_repo.get(db=db, id=id)
        if not competency_bank_form_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="competency_bank_form not found")
        competency_bank_form_ = competency_bank_form_repo.update(db=db, db_obj=competency_bank_form_, obj_in=competency_bank_form)
        return competency_bank_form_

    def get_competency_bank_form(self, *, db: Session, id: UUID) -> CompetencyBankSchema:
        competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
        if not competency_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="competency_bank_form not found")
        return competency_bank_form

    def delete_competency_bank_form(self, *, db: Session, id: UUID) -> CompetencyBankSchema:
        competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
        if not competency_bank_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="competency_bank_form not found")
        competency_bank_form = competency_bank_form_repo.remove(db=db, id=id)
        return competency_bank_form

    def get_competency_bank_form_by_id(self, *, id: UUID) -> CompetencyBankSchema:
        competency_bank_form = competency_bank_form_repo.get(id)
        if not competency_bank_form:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="competency_bank_form not found"
            )
        return competency_bank_form

    def get_competency_bank_form_by_keywords(self, *, db: Session, tag: str) -> List[CompetencyBankSchema]:
        pass

    def search_competency_bank_form(self, *, db: Session, search: str, value: str) -> List[CompetencyBankSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return competency_bank_form_repo.get_by_kwargs(self, db, kwargs)


competency_bank_form_service = CompetencyBankService()
















# from typing import List, Any

# from fastapi import Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from db.base_class import UUID
# from domains.appraisal.respository.competency_bank import competency_bank_form_actions as competency_bank_form_repo
# from domains.appraisal.schemas.competency_bank import CompetencyBankSchema, CompetencyBankCreate, CompetencyBankUpdate
# from db.session import get_db
# from ..models import competency_bank

# class CompetencyBankService:


#     def list_competency_bank_form(  db: Session=Depends(get_db), skip: int = 0, limit: int = 100) -> List[ CompetencyBankSchema]:
#         competency_bank_form = competency_bank_form_repo.get_all(db=db, skip=skip, limit=limit)
#         return  competency_bank_form

#     def create_competency_bank_form( *, db,  competency_bank_form) ->  CompetencyBankSchema:
        
#         # competency_bank_form = competency_bank_form_repo.create(db=db, obj_in= competency_bank_form)
#         competency_bank_formm =competency_bank.CompetencyBank(**competency_bank_form.dict())
#         db.add(competency_bank_formm)
#         db.commit()
#         db.refresh(competency_bank_formm)
#         return  competency_bank_formm

#     def update_competency_bank_form(self, *, db: Session, id: UUID,  competency_bank_form:CompetencyBankUpdate) ->  CompetencyBankSchema:
#         competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
#         if not  competency_bank_form:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" competency_bank_form not found")
#         competency_bank_form = competency_bank_form_repo.update(db=db, db_obj= competency_bank_form, obj_in= competency_bank_form)
#         return  competency_bank_form

#     def get_competency_bank_form( *, db: Session, id: UUID) ->  CompetencyBankSchema:
#         competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
#         if not  competency_bank_form:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" competency_bank_form not found")
#         return  competency_bank_form

#     def delete_competency_bank_form( *, db: Session, id: UUID) ->  CompetencyBankSchema:
#         competency_bank_form = competency_bank_form_repo.get(db=db, id=id)
#         if not  competency_bank_form:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" competency_bank_form not found")
#         competency_bank_form = competency_bank_form_repo.remove(db=db, id=id)
#         return  competency_bank_form

#     def get_competency_bank_form_by_id(self, *, id: UUID) ->  CompetencyBankSchema:
#         competency_bank_form = competency_bank_form_repo.get(id)
#         if not  competency_bank_form:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=" competency_bank_form not found"
#             )
#         return  competency_bank_form

#     def get_competency_bank_form_by_keywords(self, *, db: Session, tag: str) -> List[ CompetencyBankSchema]:
#         pass

#     def search_competency_bank_form(self, *, db: Session, search: str, value: str) -> List[ CompetencyBankSchema]:
#         pass

#     def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
#         return competency_bank_form_repo.get_by_kwargs(self, db, kwargs)


# competency_bank_forms_service = CompetencyBankService