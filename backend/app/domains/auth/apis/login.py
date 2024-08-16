from fastapi import APIRouter,Depends,status,Response,Cookie,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from domains.auth.schemas import auth as schema
from sqlalchemy.orm import Session
from db.session import get_db



# Authentication module for admins and users
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)








@auth_router.post("/refresh", response_model=schema.RefreshTokenResponse)
def get_new_access_token(response:Response, access_token: schema.Token, db: Session = Depends(get_db)):

    return ""