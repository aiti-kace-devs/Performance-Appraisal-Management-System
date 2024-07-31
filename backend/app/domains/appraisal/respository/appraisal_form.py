from crud.base import CRUDBase
from domains.appraisal.models.appraisal_form import Appraisal_form
from domains.appraisal.schemas.appraisal_form import (
    AppraisalFormCreate, AppraisalFormUpdate
)


class CRUDSAppraisalForm(CRUDBase[Appraisal_form, AppraisalFormCreate, AppraisalFormUpdate]):
    pass
Appraisal_form_actions = CRUDSAppraisalForm(Appraisal_form)