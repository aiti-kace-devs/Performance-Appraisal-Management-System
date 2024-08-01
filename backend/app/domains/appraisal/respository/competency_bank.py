from crud.base import CRUDBase
from domains.appraisal.models.competency_bank import CompetencyBank
from domains.appraisal.schemas.competency_bank import (
    CompetencyBankCreate, CompetencyBankUpdate
)


class CRUDCompetencyBank(CRUDBase[CompetencyBank, CompetencyBankCreate, CompetencyBankUpdate]):
    pass
competency_bank_form_actions = CRUDCompetencyBank(CompetencyBank)