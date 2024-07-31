
from domains.appraisal.apis.appraisal_submission import appraisal_submissions_router
from domains.appraisal.apis.appraisal import appraisals_router
from domains.appraisal.apis.appraisal_cycle import appraisal_cycles_router
from domains.appraisal.apis.appraisal_configuration import appraisal_configuration_router
from domains.appraisal.apis.appraisal_section import appraisal_sections_router
from domains.appraisal.apis.staff_permissions import staff_permission_router
from fastapi import APIRouter




router = APIRouter()
router.include_router(appraisal_submissions_router)
router.include_router(appraisals_router)
router.include_router(appraisal_cycles_router)
router.include_router(appraisal_configuration_router)
router.include_router(appraisal_sections_router)
router.include_router(staff_permission_router)

