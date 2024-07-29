from crud.base import CRUDBase
from domains.appraisal.models.staff import Staff
from domains.appraisal.schemas.staff import (
    StaffCreate, StaffUpdate
)


class CRUDStaff(CRUDBase[Staff, StaffCreate, StaffUpdate]):
    pass
Staff_form_actions = CRUDStaff(Staff)