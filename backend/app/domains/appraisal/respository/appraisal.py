from crud.base import CRUDBase
from domains.appraisal.models.appraisal import Appraisal
from domains.appraisal.schemas.appraisal import (
    AppraisalFormCreate, AppraisalFormUpdate
)


class CRUDAppraisalForm(CRUDBase[Appraisal, AppraisalFormCreate, AppraisalFormUpdate]):
    pass
appraisal_form_actions = CRUDAppraisalForm(Appraisal)