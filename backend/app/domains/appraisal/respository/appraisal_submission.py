from crud.base import CRUDBase
from domains.appraisal.models.appraisal_submission import AppraisalSubmission
from domains.appraisal.schemas.appraisal_submission import (
    AppraisalSubmissionCreate, AppraisalSubmissionUpdate
)


class CRUDAppraisalSubmission(CRUDBase[AppraisalSubmission, AppraisalSubmissionCreate, AppraisalSubmissionUpdate]):
    pass
appraisal_submission_actions = CRUDAppraisalSubmission(AppraisalSubmission)