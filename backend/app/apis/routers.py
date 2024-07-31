
from domains.appraisal.apis.appraisal import appraisal_forms_router
from domains.appraisal.apis.users import users_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_forms_router)
router.include_router(users_router)

