
from domains.appraisal.apis.appraisal import appraisal_forms_router
from domains.appraisal.apis.appraisal_cycle import appraisal_cycles_router
from domains.appraisal.apis.appraisal_configuration import appraisal_configuration_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_forms_router)
router.include_router(appraisal_cycles_router)
router.include_router(appraisal_configuration_router)


