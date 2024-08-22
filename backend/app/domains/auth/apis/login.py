from fastapi import APIRouter,Depends,status,Response,Cookie,Request
from domains.auth.services.user_account import users_forms_service
from domains.auth.models.refresh_token import RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from domains.auth.schemas import auth as schema
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from config.settings import settings
from utils.security import Security
from sqlalchemy.orm import Session
from datetime import timedelta
from db.session import get_db
from domains.auth.services import login as login_service




# Authentication module for admins and users
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)








@auth_router.post("/refresh")
def get_new_access_token(response:Response, refresh_token: schema.RefreshToken, db: Session = Depends(get_db)):

    token_dict = login_service.get_new_access_token(response, refresh_token, db)
    return token_dict







@auth_router.post("/current_user")
def get_current_user_by_access_token(token:schema.AccessToken, request: Request,db: Session = Depends(get_db)):

    current_user = login_service.get_current_user_by_access_token(token, request, db)
    return current_user