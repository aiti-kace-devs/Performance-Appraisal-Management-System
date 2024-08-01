from crud.base import CRUDBase
from domains.appraisal.models.appraisal import Appraisal
from domains.appraisal.schemas.appraisal import (
    AppraisalCreate, AppraisalUpdate
)


class CRUDAppraisal(CRUDBase[Appraisal, AppraisalCreate, AppraisalUpdate]):
    pass
kra_bank_form_actions = CRUDAppraisal(Appraisal)