from typing import List, Any
import json
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
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

    # def create_competency_bank_form(self, *, db: Session, competency_bank_form: CompetencyBankCreate) -> CompetencyBankSchema:

    #     competency_bank = competency_bank_form_repo.create(db=db, obj_in=competency_bank_form)
    #     return competency_bank


    def create_competency_bank_form(self, db: Session, payload: CompetencyBankCreate, **kw):

        obj_in_data = jsonable_encoder(payload, **kw)
        json_data = jsonable_encoder({key: item for key, item in enumerate(payload.competency_type)})

        new_competency = CompetencyBank(**obj_in_data)
        new_competency.competency_type = json.dumps(json_data)
        new_competency.created_by = None
        db.add(new_competency)
        db.commit()
        db.refresh(new_competency)
        return new_competency



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
    


    def get_competency_bank_by_id(self, db: Session, id: UUID) -> CompetencyBankSchema:
        
        data = db.query(CompetencyBank).filter(CompetencyBank.id == id).first()
        if not data:
            data = []
            return {
            "data": data
            }
    
        competency_type = json.loads(data.competency_type)

        return {
                "id": data.id,
                "created_by": data.created_by,
                "competency_type": [competency_type]
            }
    

    # def get_competency_bank_form_by_id(self, *, id: UUID) -> CompetencyBankSchema:
    #     competency_bank_form = competency_bank_form_repo.get(id)
    #     if not competency_bank_form:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="competency_bank_form not found"
    #         )
    #     return competency_bank_form

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