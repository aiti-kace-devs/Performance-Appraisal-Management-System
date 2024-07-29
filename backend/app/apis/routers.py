
from domains.appraisal.apis.appraisal import appraisal_forms_router
from domains.appraisal.apis.roles import role_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_forms_router)
router.include_router(role_router)


