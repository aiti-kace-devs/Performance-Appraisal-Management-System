from crud.base import CRUDBase
from domains.appraisal.models.competency_bank import CompentencyBank
from domains.appraisal.schemas.competency_bank import (
    CompentencyBankCreate, CompentencyBankUpdate
)


class CRUDCompentencyBank(CRUDBase[CompentencyBank, CompentencyBankCreate, CompentencyBankUpdate]):
    pass
competency_bank_form_actions = CRUDCompentencyBank(CompentencyBank)