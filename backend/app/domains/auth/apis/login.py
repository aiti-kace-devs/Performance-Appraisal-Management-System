from fastapi import APIRouter,Depends,status,Response,Cookie,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from domains.auth.schemas import auth as schema
from sqlalchemy.orm import Session
from db.session import get_db
from domains.auth.models.refresh_token import RefreshToken
from domains.auth.services.user_account import users_forms_service

# Authentication module for admins and users
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)








@auth_router.post("/refresh", response_model=schema.RefreshTokenResponse)
def get_new_access_token(response:Response, access_token: schema.Token, db: Session = Depends(get_db)):

    refresh_token_check = db.query(RefreshToken).filter(RefreshToken.refresh_token == access_token.access_token).first()
    if not refresh_token_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Could not validate new access token credentials",
                        headers={"WWW-Authenticate": "Bearer"}
                        )
    
    user_data = users_forms_service.get_user_by_id(db=db, id=refresh_token_check.id)
    

    return ""