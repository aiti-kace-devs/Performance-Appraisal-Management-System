
from domains.appraisal.apis.appraisal import appraisals_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisals_router)


