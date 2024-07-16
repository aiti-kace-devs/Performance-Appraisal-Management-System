from crud.base import CRUDBase
from backend.app.domains.appraisal.models.appraisal import AppraisalForm
from backend.app.domains.appraisal.schemas.appraisal import (
    AppraisalFormCreate, AppraisalFormUpdate
)


class CRUDAppraisalForm(CRUDBase[AppraisalForm, AppraisalFormCreate, AppraisalFormUpdate]):
    pass
appraisal_form_actions = CRUDAppraisalForm(AppraisalForm)