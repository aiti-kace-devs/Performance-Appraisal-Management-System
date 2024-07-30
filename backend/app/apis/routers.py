
from domains.appraisal.apis.appraisal import appraisal_forms_router
from domains.appraisal.apis.staff_deadline import staff_deadline_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(staff_deadline_router)


