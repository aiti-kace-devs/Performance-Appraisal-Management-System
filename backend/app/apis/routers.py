
from domains.appraisal.apis.appraisal_form import appraisal_form_router
from domains.appraisal.apis.appraisal_submission import appraisal_submissions_router
from domains.appraisal.apis.department import department_router
from domains.appraisal.apis.appraisal import appraisals_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_form_router)
router.include_router(appraisal_submissions_router)
router.include_router(department_router)
router.include_router(appraisals_router)


