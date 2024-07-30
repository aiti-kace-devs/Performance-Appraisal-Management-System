from crud.base import CRUDBase
from domains.appraisal.models.staff_deadline import StaffDeadline
from domains.appraisal.schemas.staff_deadline import (
    StaffDeadlineCreate, StaffDeadlineUpdate
)


class CRUDStaffDeadline(CRUDBase[StaffDeadline, StaffDeadlineCreate, StaffDeadlineUpdate]):
    pass
staff_deadline_actions = CRUDStaffDeadline(StaffDeadline)
