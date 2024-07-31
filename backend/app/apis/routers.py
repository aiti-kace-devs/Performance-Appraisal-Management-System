
from domains.appraisal.apis.department import department_router
from fastapi import APIRouter
from domains.appraisal.apis.staff_permissions import staff_permission_router





router = APIRouter()
router.include_router(department_router)


