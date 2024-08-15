from fastapi import APIRouter,Depends,status,Response,Cookie,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException






# Authentication module for admins and users
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)