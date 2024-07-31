
from domains.appraisal.apis.department import department_router
from fastapi import APIRouter





router = APIRouter()
router.include_router(department_router)


