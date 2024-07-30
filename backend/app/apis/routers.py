
from domains.appraisal.apis.appraisal import appraisal_forms_router
from fastapi import APIRouter 
from domains.appraisal.apis.staff_permissions import staff_permission_router





router = APIRouter()
router.include_router(appraisal_forms_router)
router.include_router(staff_permission_router)

