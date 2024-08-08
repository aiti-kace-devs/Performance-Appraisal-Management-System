from crud.base import CRUDBase
from domains.appraisal.models.role_permissions import Role
from domains.appraisal.schemas.roles import (
    RoleCreate, RoleUpdate
)


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    pass
role_actions = CRUDRole(Role)