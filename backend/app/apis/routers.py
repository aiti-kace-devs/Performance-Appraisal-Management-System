
from domains.appraisal.apis.appraisal_submission import appraisal_submissions_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_submissions_router)


