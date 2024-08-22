from typing import List, Any
import re
from jose import JWTError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.base_class import UUID
from domains.auth.respository.login import logged_in_users_actions as logged_in_users_repo
from domains.auth.schemas.user_account import UserSchema
from datetime import timedelta, datetime, timezone
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
        

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        
        # Ensure datetime.now() is timezone-aware by setting it to UTC
        now_utc = datetime.now()
        print("now_utc: ", now_utc)
        
        print("user in log: ", user.failed_login_attempts)
        print("user account locked until: ", user.account_locked_until)
        print("is user account blocked? ", user.is_account_locked())

        
        if user.is_account_locked():
            if now_utc < user.account_locked_until:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is locked due to multiple failed login attempts.",
                )
            else:
                # Unlock the account if the lock time has passed
                user.reset_failed_attempts()
                user.account_locked_until = None
                db.commit()

        if not Security.verify_password(form_data.password, user.password):
            user.failed_login_attempts += 1
            print("Failed login attempts incremented to:", user.failed_login_attempts)

            if user.failed_login_attempts >= 3:
                user.lock_account(lock_time_minutes=10)
                db.commit()
                
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is locked due to multiple failed login attempts.",
                )
            
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        # Reset failed attempts after successful login
        user.reset_failed_attempts()
        db.commit()
        
        # Token creation logic
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)
        
        if form_data.scopes and "remember_me" in form_data.scopes:
            refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_REMEMBER_ME_DAYS)

        access_token = Security.create_access_token(
            data={"sub": str(user.email)}, expires_delta=access_token_expires
        )
        refresh_token = Security.create_refresh_token(
            data={"sub": str(user)}, expires_delta=refresh_token_expires
        )


        expiration_time = datetime.now(timezone.utc) + refresh_token_expires

        db_refresh_token = db.query(RefreshToken).filter(RefreshToken.user_id == user.id).first()
        if db_refresh_token:
            db_refresh_token.refresh_token = refresh_token
            db_refresh_token.expiration_time = expiration_time
        else:
            db_refresh_token = RefreshToken(user_id=user.id, refresh_token=refresh_token, expiration_time=expiration_time)
            db.add(db_refresh_token)

        db.commit()

        # Set cookies for access and refresh tokens
        response.set_cookie(key="AccessToken", value=access_token, httponly=True, secure=True, samesite='none', expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key="RefreshToken", value=refresh_token, httponly=True, secure=True, samesite='none', expires=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "access_token_expiration": access_token_expires,
            "user": {
                "id": user.id, 
                "email": user.email,
                "role": user.role_id
            },
            "refresh_token": refresh_token,
            "refresh_token_expiration": expiration_time
        }
    



    


login_service = LoginService()