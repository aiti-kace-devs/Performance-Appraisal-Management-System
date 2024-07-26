from crud.base import CRUDBase
from domains.appraisal.models.department import Department
from domains.appraisal.schemas.department import (
    DepartmentCreate, DepartmentUpdate
)


class CRUDAppraisal(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    pass
department_actions = CRUDAppraisal(Department)