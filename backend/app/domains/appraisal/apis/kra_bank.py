from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.schemas import appraisal as schemas
from domains.appraisal.services.appraisal import appraisal_form_service as actions
from db.session import get_db


appraisal_forms_router = APIRouter(
       prefix="/kra_bank",
    tags=["Kra Bank"],
    responses={404: {"description": "Not found"}},
)


