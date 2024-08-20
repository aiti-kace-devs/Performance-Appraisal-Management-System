from typing import List, Any
import re
from jose import JWTError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.base_class import UUID
from domains.auth.respository.login import logged_in_users_actions as logged_in_users_repo
from domains.auth.schemas.user_account import UserSchema
from datetime import timedelta
from fastapi import Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import Security
from domains.auth.models.users import User
from domains.auth.models.refresh_token import RefreshToken
from db.session import get_db
from config.settings import settings
from fastapi.encoders import jsonable_encoder


class LoginService:


    def get_tokens(self, request: Request):
        # Extract tokens from cookies
        access_token = request.cookies.get("AccessToken")
        refresh_token = request.cookies.get("RefreshToken")

        return {
            "AccessToken": access_token,
            "RefreshToken": refresh_token
        }
    

    def list_logged_in_users(self,  request: Request, db: Session = Depends(get_db), skip: int = 0, limit: int = 100) :
         # Fetch tokens from cookies
        tokens = login_service.get_tokens(request)

        if not tokens['AccessToken'] or not tokens['RefreshToken']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")

        user_email = None

        # Verify Access Token
        try:
            payload = Security.decode_token(tokens['AccessToken'])
            user_email = payload.get("sub")
        except JWTError:
            # If Access Token is invalid, try verifying the Refresh Token
            try:
                payload = Security.decode_token(tokens['RefreshToken'])
                user = payload.get("sub")
                if user:
                    user_email = user.email  # Extract email from user object
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid tokens")

        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to determine logged-in user")

        # Query to list all users with active refresh tokens
        logged_in_users = db.query(User).join(RefreshToken, User.id == RefreshToken.user_id).offset(skip).limit(limit).all()

        # Format the output
        user_list = [
            {
                "staff_id": user.staff_id,
                "email": user.email,
                "role_id": user.role_id
            }
            for user in logged_in_users
        ]

        return {"logged_in_users": user_list}



    def log_user_in(self, response: Response, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
        user = db.query(User).filter(User.email == form_data.username).first()

        if not user or not Security.verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if user.is_account_locked():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is locked due to multiple failed login attempts.",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)
        
        # Extend refresh token expiration for "Remember Me"
        if form_data.scopes and "remember_me" in form_data.scopes:
            refresh_token_expires = timedelta(days=settings.refresh_token_remember_me_days)

        access_token = Security.create_access_token(
            data={"sub": str(user.email)}, expires_delta=access_token_expires
        )
        refresh_token = Security.create_refresh_token(
            data={"sub": str(user)}, expires_delta=refresh_token_expires
        )

        # Store or update the refresh token in the database
        db_refresh_token = db.query(RefreshToken).filter(RefreshToken.user_id == user.id).first()
        if db_refresh_token:
            db_refresh_token.refresh_token = refresh_token
        else:
            db_refresh_token = RefreshToken(user_id=user.id, refresh_token=refresh_token)
            db.add(db_refresh_token)

        db.commit()

        
        
        # Set cookies for access and refresh tokens
        response.set_cookie(key="AccessToken", value=access_token, httponly=True, expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key="RefreshToken", value=refresh_token, httponly=True, expires=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)
        #response = {"access_token": access_token, "token_type": "bearer"}
        return {
        "access_token":access_token,
        "token_type": "bearer",
        "user": {"id": user.id, 
                 "email": user.email,
                "role": user.role_id
                },
        "refresh_token":refresh_token,
        "response": response
        }
    



    


login_service = LoginService()