from domains.appraisal.apis.appraisal_configuration import appraisal_configuration_router
from domains.appraisal.apis.appraisal_submission import appraisal_submissions_router
from domains.appraisal.apis.competency_bank import competency_bank_forms_router
from domains.appraisal.apis.appraisal_section import appraisal_sections_router
from domains.appraisal.apis.staff_permissions import staff_permission_router
from domains.appraisal.apis.appraisal_cycle import appraisal_cycles_router
from domains.appraisal.apis.staff_deadline import staff_deadline_router
from domains.appraisal.apis.appraisal_form import appraisal_form_router
from domains.appraisal.apis.role_permission import role_perm_router
from domains.appraisal.apis.department import department_router
from domains.appraisal.apis.appraisal import appraisals_router
from domains.appraisal.apis.kra_bank import kra_bank_router
from domains.appraisal.apis.permissions import perm_router
from domains.auth.apis.user_account import users_router
from domains.appraisal.apis.staff import staff_router
from domains.appraisal.apis.roles import role_router
from domains.auth.apis.login import auth_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(auth_router)
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
router.include_router(kra_bank_router)
# router.include_router(role_perm_router)
router.include_router(role_perm_router)
router.include_router(role_router)
router.include_router(perm_router)


