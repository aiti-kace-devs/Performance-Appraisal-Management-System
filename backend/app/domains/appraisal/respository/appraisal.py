from crud.base import CRUDBase
from domains.appraisal.models.kra_bank import KraBank
from domains.appraisal.schemas.kra_bank import KraBankCreate, KraBankUpdate


class CRUDKra_Bank(CRUDBase[KraBank, KraBankCreate, KraBankUpdate]):
    pass


appraisal_form_actions = CRUDKra_Bank(KraBank)
