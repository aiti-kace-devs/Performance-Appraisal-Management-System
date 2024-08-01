from crud.base import CRUDBase
<<<<<<< HEAD
from domains.appraisal.models.kra_bank import KraBank
from domains.appraisal.schemas.kra_bank import KraBankCreate, KraBankUpdate


class CRUDKra_Bank(CRUDBase[KraBank, KraBankCreate, KraBankUpdate]):
    pass


appraisal_form_actions = CRUDKra_Bank(KraBank)
=======
from domains.appraisal.models.appraisal import Appraisal
from domains.appraisal.schemas.appraisal import (
    AppraisalCreate, AppraisalUpdate
)


class CRUDAppraisal(CRUDBase[Appraisal, AppraisalCreate, AppraisalUpdate]):
    pass
appraisal_actions = CRUDAppraisal(Appraisal)
>>>>>>> 0ab3f152a475199175e363c26417debb069e72b0
