from crud.base import CRUDBase
from domains.appraisal.models.staff_permissions import StaffPermission
from domains.appraisal.schemas.staff_permissions import (StaffPermissionCreate, StaffPermissionUpdate)


class CRUDStaffPermission(CRUDBase[StaffPermission, StaffPermissionCreate, StaffPermissionUpdate]):
    pass

staff_permission_action = CRUDStaffPermission(StaffPermission)

