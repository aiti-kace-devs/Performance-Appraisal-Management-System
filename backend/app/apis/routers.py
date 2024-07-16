
from domains.appraisal.apis.appraisal import appraisal_forms_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_forms_router)


