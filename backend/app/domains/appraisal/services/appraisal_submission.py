from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.appraisal.respository.appraisal_submission import appraisal_submission_actions as appraisal_submission_repo
from domains.appraisal.schemas.appraisal_submission import AppraisalSubmissionSchema, AppraisalSubmissionUpdate, AppraisalSubmissionCreate


class AppraisalService:


    def list_appraisal_submission(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalSubmissionSchema]:
        appraisal_submission = appraisal_submission_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_submission

    def create_appraisal_submission(self, *, db: Session, appraisal_submission: AppraisalSubmissionCreate) -> AppraisalSubmissionSchema:
        appraisal_submission = appraisal_submission_repo.create(db=db, obj_in=appraisal_submission)
        return appraisal_submission

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