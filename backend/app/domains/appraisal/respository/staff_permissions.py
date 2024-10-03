from crud.base import CRUDBase
from domains.appraisal.models.staff_role_permissions import staff_permissions
# from domains.appraisal.models.staff_permissions import StaffPermission
from domains.appraisal.schemas.staff_permissions import (StaffPermissionCreate, StaffPermissionUpdate)


class CRUDStaffPermission(CRUDBase[staff_permissions, StaffPermissionCreate, StaffPermissionUpdate]):
    pass

staff_permission_action = CRUDStaffPermission(staff_permissions)
