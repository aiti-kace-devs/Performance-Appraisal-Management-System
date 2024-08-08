
from domains.appraisal.apis.appraisal import appraisal_forms_router
from domains.appraisal.apis.roles import role_router
from domains.appraisal.apis.permissions import perm_router
from domains.appraisal.apis.role_permission import role_perm_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(appraisal_forms_router)
router.include_router(role_perm_router)
router.include_router(role_router)
router.include_router(perm_router)


