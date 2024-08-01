from crud.base import CRUDBase
from domains.appraisal.models.appraisal_form import AppraisalForm
from domains.appraisal.schemas.appraisal_form import (
    AppraisalFormCreate, AppraisalFormUpdate
)


class CRUDSAppraisalForm(CRUDBase[AppraisalForm, AppraisalFormCreate, AppraisalFormUpdate]):
    pass
Appraisal_form_actions = CRUDSAppraisalForm(AppraisalForm)