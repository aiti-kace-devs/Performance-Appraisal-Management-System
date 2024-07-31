
from domains.appraisal.apis.appraisal import appraisals_router
from fastapi import APIRouter
from domains.appraisal.apis.staff_permissions import staff_permission_router





router = APIRouter()
router.include_router(appraisals_router)


