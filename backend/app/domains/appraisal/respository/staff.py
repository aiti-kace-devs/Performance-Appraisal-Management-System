from crud.base import CRUDBase
from domains.appraisal.models.staff_role_permissions import Staff
from domains.appraisal.schemas.staff import (
    StaffCreate, StaffUpdate
)


class CRUDStaff(CRUDBase[Staff, StaffCreate, StaffUpdate]):
    pass
Staff_form_actions = CRUDStaff(Staff)