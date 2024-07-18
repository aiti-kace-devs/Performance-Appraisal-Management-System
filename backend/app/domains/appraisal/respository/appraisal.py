from crud.base import CRUDBase
from domains.appraisal.models.appraisal import AppraisalForm
from domains.appraisal.schemas.appraisal import (
    AppraisalFormCreate, AppraisalFormUpdate
)


class CRUDAppraisalForm(CRUDBase[AppraisalForm, AppraisalFormCreate, AppraisalFormUpdate]):
    pass
appraisal_form_actions = CRUDAppraisalForm(AppraisalForm)