from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from db.base_class import UUID
from domains.appraisal.respository.appraisal_submission import appraisal_submission_actions as appraisal_submission_repo
from domains.appraisal.schemas.appraisal_submission import AppraisalSubmissionSchema, AppraisalSubmissionUpdate, AppraisalSubmissionCreate
from domains.appraisal.models.appraisal_submission import AppraisalSubmission
from domains.appraisal.models.staff_role_permissions import Staff
from domains.appraisal.models.appraisal_form import AppraisalForm



class AppraisalService:


    def list_appraisal_submission(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalSubmissionSchema]:
        appraisal_submission = appraisal_submission_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_submission

    def create_appraisal_submission(self, db: Session, payload: AppraisalSubmissionCreate,  **kw):

        check_if_staff_exist = db.query(Staff).filter(Staff.id == payload.submitted_by).first()
        if not check_if_staff_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Staff not found")
        
        check_appraisal_form_id = db.query(AppraisalForm).filter(AppraisalForm.id == payload.appraisal_forms_id).first()
        if not check_appraisal_form_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Appraisal form not found")


        obj_in_data = jsonable_encoder(payload, **kw)
        json_data = jsonable_encoder(payload.submitted_values)
        new_submitted_values = AppraisalSubmission(**obj_in_data)
        new_submitted_values.submitted_values = json_data
        new_submitted_values.submitted_by = check_if_staff_exist.id
        new_submitted_values.appraisal_forms_id = payload.appraisal_forms_id
        new_submitted_values.started_at = payload.started_at
        new_submitted_values.completed_at = payload.completed_at
        new_submitted_values.approval_date = payload.approval_date
        new_submitted_values.submitted = payload.submitted
        new_submitted_values.completed = payload.completed
        new_submitted_values.approval_status = payload.approval_status
        new_submitted_values.comment = payload.comment
        db.add(new_submitted_values)
        db.commit()
        db.refresh(new_submitted_values)

        return {
            "id": new_submitted_values.id,
            "submitted_by": {
                "id": new_submitted_values.staffs.id,
                "first_name": new_submitted_values.staffs.first_name,
                "last_name": new_submitted_values.staffs.last_name,
                "other_name": new_submitted_values.staffs.other_name,
                "full_name": f"{new_submitted_values.staffs.first_name} {new_submitted_values.staffs.last_name}" + (f" {new_submitted_values.staffs.other_name}" if new_submitted_values.staffs.other_name else ""),
                "email": new_submitted_values.staffs.email,
            },
            "appraisal_forms_id": new_submitted_values.appraisal_forms_id,
            "submitted_values": new_submitted_values.submitted_values,
            "started_at": new_submitted_values.started_at,
            "completed_at": new_submitted_values.completed_at,
            "approval_date": new_submitted_values.approval_date,
            "submitted": new_submitted_values.submitted,
            "completed": new_submitted_values.completed,
            "approval_status": new_submitted_values.approval_status,
            "comment": new_submitted_values.comment,
        }






    def update_appraisal_submission(self, *, db: Session, id: UUID, appraisal_submission: AppraisalSubmissionUpdate) -> AppraisalSubmissionSchema:
        appraisal_submission_ = appraisal_submission_repo.get(db=db, id=id)
        if not appraisal_submission_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_submission not found")
        appraisal_submission = appraisal_submission_repo.update(db=db, db_obj=appraisal_submission_, obj_in=appraisal_submission)
        return appraisal_submission

    def get_appraisal_submission(self, *, db: Session, id: UUID) -> AppraisalSubmissionSchema:
        appraisal_submission = appraisal_submission_repo.get(db=db, id=id)
        if not appraisal_submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_submission not found")
        return appraisal_submission

    def delete_appraisal_submission(self, *, db: Session, id: UUID) -> AppraisalSubmissionSchema:
        appraisal_submission = appraisal_submission_repo.get(db=db, id=id)
        if not appraisal_submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_submission not found")
        appraisal_submission = appraisal_submission_repo.remove(db=db, id=id)
        return appraisal_submission

    def get_appraisal_submission_by_id(self, *, id: UUID) -> AppraisalSubmissionSchema:
        appraisal_submission = appraisal_submission_repo.get(id)
        if not appraisal_submission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="appraisal_submission not found"
            )
        return appraisal_submission

    def get_appraisal_submission_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalSubmissionSchema]:
        pass

    def search_appraisal_submission(self, *, db: Session, search: str, value: str) -> List[AppraisalSubmissionSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return appraisal_submission_repo.get_by_kwargs(self, db, kwargs)


appraisal_submission_service = AppraisalService()