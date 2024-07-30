from crud.base import CRUDBase
from domains.appraisal.models.role_permissions import RolePermission
from domains.appraisal.schemas.role_permissions import (
   RolePermissionBase, RolePermissionCreate, RolePermissionUpdate

)


class CRUDRole(CRUDBase[RolePermission, RolePermissionCreate, RolePermissionUpdate]):
    pass
role_perm_actions = CRUDRole(RolePermission)