from crud.base import CRUDBase
from domains.appraisal.models.staff_role_permissions import role_permissions
from domains.appraisal.schemas.role_permissions import (
   RolePermissionBase, RolePermissionCreate, RolePermissionUpdate

)


class CRUDRole(CRUDBase[role_permissions, RolePermissionCreate, RolePermissionUpdate]):
    pass
role_perm_actions = CRUDRole(role_permissions)