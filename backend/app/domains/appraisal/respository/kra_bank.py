from crud.base import CRUDBase
from domains.appraisal.models.kra_bank import KraBank
from domains.appraisal.schemas.kra_bank import KraBankBaseCreate, KraBankUpdate


class CRUDKraBank(CRUDBase[KraBank, KraBankBaseCreate, KraBankUpdate]):
    pass


kra_bank_actions = CRUDKraBank(KraBank)
