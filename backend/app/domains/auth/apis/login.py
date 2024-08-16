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





# Authentication module for admins and users
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)








@auth_router.post("/refresh")
def get_new_access_token(response:Response, refresh_token: schema.Token, db: Session = Depends(get_db)):

    refresh_token_check = db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token.refresh_token).first()
    if not refresh_token_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Could not validate new access token credentials",
                        headers={"WWW-Authenticate": "Bearer"}
                        )
    
    # Get current user information
    user_data = users_forms_service.get_user_by_id(db=db, id=refresh_token_check.user_id)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = Security.create_access_token(data={"email": user_data.email}, expires_delta=access_token_expires)
    new_refresh_token = Security.create_refresh_token(jsonable_encoder(user_data))


    # Set Cookie for new access token
    response.set_cookie(
        key="AccessToken",
        value=new_access_token,
        samesite='none',
        httponly=True,
        expires=settings.COOKIE_ACCESS_EXPIRE,
        # domain=settings.COOKIE_DOMAIN,
        secure=True
    )

    # Set Cookie for new refresh token
    response.set_cookie(
        key="RefreshToken",
        value=new_refresh_token,
        samesite='none',
        httponly=True,
        expires=settings.COOKIE_REFRESH_EXPIRE,
        # domain=settings.COOKIE_DOMAIN,
        secure=True
    )


    # delete user refresh token after requesting for a new access token
    refresh_token_check = db.query(RefreshToken).filter(RefreshToken.user_id == user_data.id)
    if refresh_token_check.first():
        refresh_token_check.delete()
        db.commit()


    refresh_token_dict = {
        "user_id": user_data.id,
        "refresh_token": new_refresh_token,
    }

    # create new refresh token for user after requesting for a new access token
    refresh_token_data= RefreshToken(**refresh_token_dict)
    db.add(refresh_token_data)
    db.commit()
    

    return {
        "access_token": new_access_token,
        "token_type":"bearer",
        "refresh_token":new_refresh_token,
        "status": status.HTTP_200_OK
        }