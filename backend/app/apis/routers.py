
from domains.appraisal.apis.staff import staff_router
from fastapi import APIRouter




router = APIRouter()
router.include_router(staff_router)


