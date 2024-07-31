
from domains.appraisal.apis.appraisal_form import appraisal_form_router
from fastapi import APIRouter




router = APIRouter()
router.include_router(appraisal_form_router)


