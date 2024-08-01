from domains.appraisal.apis.appraisal_submission import appraisal_submissions_router
from domains.appraisal.apis.appraisal import appraisals_router
from domains.appraisal.apis.appraisal_cycle import appraisal_cycles_router
from domains.appraisal.apis.appraisal_configuration import appraisal_configuration_router
from domains.appraisal.apis.appraisal_section import appraisal_sections_router
from domains.appraisal.apis.staff_permissions import staff_permission_router
from domains.appraisal.apis.department import department_router
from domains.appraisal.apis.staff_deadline import staff_deadline_router
from domains.appraisal.apis.competency_bank import competency_bank_forms_router
from domains.appraisal.apis.users import users_router
from domains.appraisal.apis.staff import staff_router
from domains.appraisal.apis.appraisal_form import appraisal_form_router
from fastapi import APIRouter
from domains.appraisal.apis.staff_permissions import staff_permission_router




router = APIRouter()
router.include_router(department_router)
router.include_router(staff_router)
router.include_router(users_router)
router.include_router(appraisal_cycles_router)
router.include_router(appraisals_router)
router.include_router(appraisal_configuration_router)
router.include_router(appraisal_sections_router)
router.include_router(competency_bank_forms_router)
router.include_router(appraisal_form_router)
router.include_router(appraisal_submissions_router)
router.include_router(staff_permission_router)
router.include_router(staff_deadline_router)


