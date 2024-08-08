from crud.base import CRUDBase
from domains.appraisal.models.role_permissions import Permission
from domains.appraisal.schemas.permissions import (
    PermissionCreate, PermissionUpdate
)


class CRUDRole(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    pass
perm_actions = CRUDRole(Permission)