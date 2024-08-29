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
from domains.appraisal.models.role_permissions import Role
from .user_account_mail import *
import os
import requests
import json


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


    def secure_log_intruder_info(self, intruder_info: dict):
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file_name = f"intruder_log_{current_date}.txt"
        log_directory = "security/logs/"

        # Secure the logging directory
        #os.makedirs(log_directory, mode=0o750, exist_ok=True)
        os.makedirs(log_directory,  exist_ok=True)
        log_filepath = os.path.join(log_directory, log_file_name)

        print("log directory: ", log_filepath)

        log_entry = (
            f"Timestamp: {intruder_info.get('timestamp', 'N/A')}\n"
            f"IP Address: {intruder_info.get('ip_address', 'N/A')}\n"
            f"MAC Address: {intruder_info.get('mac_address', 'N/A')}\n"
            f"User-Agent: {intruder_info.get('user_agent', 'N/A')}\n"
            f"Location: {json.dumps(intruder_info.get('location', {}))}\n"
            f"Username Attempted: {intruder_info.get('username', 'N/A')}\n"
            "\n================================================================================\n\n"
        )

        # Use a try-except block to catch potential errors
        try:
            with open(log_filepath, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
            
            print(f"successfully log intruder's info.\ninfo: {log_entry}")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    #get location data
    async def get_location_data(self, ip_address: str) -> dict:
        try:
            response = await requests.get(f"https://ipinfo.io/{ip_address}/geo")
            if response.status_code == 200:
                return response.json()
            
            print("intruder's location identified: ", response.json())
        except Exception as e:
            print(f"Error fetching location data: {e}")
        return {}
    
    
    async def log_intruder_attempt(self, username: str, request: Request):
        # try:
        #     print("finding device location...")
        #     # Asynchronous request to get location data
        #     await LoginService.get_location_data(self, request.client.host)
        #     #print("\nlocation: ", location)
        #     #return location
        # except Exception as e:
        #     print(f"Error fetching location data: {e}")
        #     location = {}

        location = {}
        try:
            response = requests.get(f"https://ipinfo.io/{request.client.host}/geo")
            if response.status_code == 200:
                print("response success: ", response)
                location = response.json()
                #return response.json()
            print("response location: ", response)
            print("intruder's location identified: ", response.json())
        except Exception as e:
            print(f"Error fetching location data: {e}")
        #return {}
        print("location: ", location)
        intruder_info = {
            "username": username,
            "ip_address": request.client.host,
            "mac_address": request.headers.get("X-MAC-Address", "N/A"),
            "user_agent": request.headers.get("User-Agent", "N/A"),
            "location": location,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Log the intruder information
        return LoginService.secure_log_intruder_info(self,intruder_info)


    async def log_user_in(self, request:Request, response: Response, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
        user = db.query(User).filter(User.email == form_data.username).first()
        print("user in log: ", user.failed_login_attempts)
        print("user account locked until: ", user.account_locked_until)
        print("is user account blocked? ", user.is_account_locked())

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account Disabled, please contact system administrator for redress.",
            )
        # Ensure datetime.now() is timezone-aware by setting it to UTC
        now_utc = datetime.now()
        print("now_utc: ", now_utc)
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
                if user.lock_count <= 2:
                    user.lock_count += 1
                elif user.lock_count >= 3:
                    user.is_active = False
                    user.lock_count = 0
                    db.commit()
                    email_body = account_emergency("")
                    await send_email(email=user.email, subject="Account Status", body=email_body)  #send email message
                
                print("lock count = ", user.lock_count)    
                db.commit()
                
                await LoginService.log_intruder_attempt(self, user.email, request)
                #await LoginService.log_intruder_attempt(user.username, request)
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
        access_token_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(seconds=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)
        print("refresh token expires: ", refresh_token_expires)
        # access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        # refresh_token_expires = settings.REFRESH_TOKEN_DURATION_IN_MINUTES
        
        if form_data.scopes and "remember_me" in form_data.scopes:
            refresh_token_expires = timedelta(days=60)
            print("refresh token expiration on remeber_me: ", refresh_token_expires)

        access_token = Security.create_access_token(
            data={"sub": str(user.email)}, expires_delta=access_token_expires
        )
        refresh_token = Security.create_refresh_token(
            data={"sub": str(user)}, expires_delta=refresh_token_expires
        )


        #expiration_time = datetime.now(timezone.utc) + refresh_token_expires
        #expiration_time = timedelta(seconds=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)

        expiration_time = datetime.now() + refresh_token_expires
        access_token_expiration = datetime.now() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        print("expiration time for refresh token: ", expiration_time)

        db_refresh_token = db.query(RefreshToken).filter(RefreshToken.user_id == user.id).first()
        if db_refresh_token:
            db_refresh_token.refresh_token = refresh_token
            db_refresh_token.expiration_time = expiration_time
        else:
            db_refresh_token = RefreshToken(user_id=user.id, refresh_token=refresh_token, expiration_time=expiration_time)
            db.add(db_refresh_token)

        db.commit()

        refresh_token_expires = expiration_time
        print("\n\nrefresh_token_expires: ",refresh_token_expires)
        # Set cookies for access and refresh tokens
        response.set_cookie(key="AccessToken", value=access_token, httponly=True, secure=True, samesite='none', expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        if form_data.scopes and "remember_me" in form_data.scopes:
            response.set_cookie(key="RefreshToken", value=refresh_token, httponly=True, secure=True, samesite='none' ,expires=(settings.REFRESH_TOKEN_DURATION_IN_MINUTES+settings.REFRESH_TOKEN_DURATION_IN_MINUTES))
        else:
            response.set_cookie(key="RefreshToken", value=refresh_token, httponly=True, secure=True, samesite='none' ,expires=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)
        
        user_role = db.query(Role).filter(Role.id == user.role_id).first()

        return {
            "access_token":  access_token,
            "token_type": "bearer",
            "access_token_expiration": access_token_expiration,
            "user": {
                "id": user.id, 
                "email": user.email,
                "role_id": user.role_id,
                "role": user_role.name
            },
            "refresh_token": refresh_token,
            "refresh_token_expiration": expiration_time
        }





    


    


login_service = LoginService()