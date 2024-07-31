
from domains.appraisal.apis.appraisal_form import appraisal_form_router
from domains.appraisal.apis.users import users_router
from domains.appraisal.apis.competency_bank import competency_bank_forms_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_form_router)
router.include_router()
router.include_router(users_router)
router.include_router(competency_bank_forms_router)


