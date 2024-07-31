
from domains.appraisal.apis.appraisal_submission import appraisal_submissions_router
from fastapi import APIRouter
from domains.appraisal.apis.staff_permissions import staff_permission_router





router = APIRouter()
router.include_router(appraisal_submissions_router)


