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



    def log_user_in(self, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
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

        response = {"access_token": access_token, "token_type": "bearer"}
        
        # Set cookies for access and refresh tokens
        response.set_cookie(key="AccessToken", value=access_token, httponly=True)
        response.set_cookie(key="RefreshToken", value=refresh_token, httponly=True, expires=refresh_token_expires)

        return response
    



    # def create_appraisal_section(self, *, db: Session, appraisal_section: AppraisalSectionCreate) -> AppraisalSectionSchema:
    #     appraisal_section = appraisal_section_repo.create(db=db, obj_in=appraisal_section)
    #     return appraisal_section

    # def update_appraisal_section(self, *, db: Session, id: UUID, appraisal_section: AppraisalSectionUpdate) -> AppraisalSectionSchema:
    #     appraisal_section_obj = appraisal_section_repo.get(db=db, id=id)
    #     if not appraisal_section_obj:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_section not found")
    #     appraisal_section_ = appraisal_section_repo.update(db=db, db_obj=appraisal_section_obj, obj_in=appraisal_section)
    #     return appraisal_section_

    # def get_appraisal_section(self, *, db: Session, id: UUID) -> AppraisalSectionSchema:
    #     appraisal_section = appraisal_section_repo.get(db=db, id=id)
    #     if not appraisal_section:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_section not found")
    #     return appraisal_section

    # def delete_appraisal_section(self, *, db: Session, id: UUID) -> AppraisalSectionSchema:
    #     appraisal_section = appraisal_section_repo.get(db=db, id=id)
    #     if not appraisal_section:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_section not found")
    #     appraisal_section = appraisal_section_repo.remove(db=db, id=id)
    #     return appraisal_section

    # def get_appraisal_section_by_id(self, *, id: UUID) -> AppraisalSectionSchema:
    #     appraisal_section = appraisal_section_repo.get(id)
    #     if not appraisal_section:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="appraisal_section not found"
    #         )
    #     return appraisal_section
    
    # # Check if value is an integer and formatted as yyyy
    # def is_valid_year(self, year_str: str) -> bool:
    #     return year_str.isdigit() and len(year_str) == 4
    

    # def iread(self, db: Session, value: str) -> List[AppraisalSection]:
    #     search_field = "name"
    #     response = []

    #     # Sanitize and validate input
    #     search_value = re.sub(r'[^\w\s]', '', value.strip())  # Remove special characters
    #     if not search_value:
    #         return response

    #     try:
    #         # Use parameterized queries to prevent SQL injection
    #         if search_field and search_value:
    #             response = db.query(AppraisalSection).filter(
    #                 getattr(AppraisalSection, search_field).ilike(f"%{search_value}%")
    #             ).all()

    #             if not response and self.is_valid_year(value.strip()):
    #                 response = db.query(AppraisalSection).filter(
    #                     AppraisalSection.year == search_value
    #                 ).all()

    #     except SQLAlchemyError as e:
    #         print(f"Database error occurred: {e}")
    #         # Log the error and return a safe message
    #         # log.error(f"Database error occurred: {e}")
    #         return {"error": "An error occurred while processing your request."}
    #     except KeyError as ke:
    #         # Log the error and return a safe message
    #         # log.error(f"Key error: {ke}")
    #         print(f"Key error: {ke}")
    #         return {"error": "Invalid search parameter."}

    #     return response
    
    # def read_appraisal_section_by_name_by_year(self, *, db:Session, search_word: str) -> List[AppraisalSectionSchema]:
    #     appraisal_section_name = self.iread(db=db, value=search_word)
    #     return appraisal_section_name
    



    # def get_appraisal_section_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalSectionSchema]:
    #     pass

    # def search_appraisal_section(self, *, db: Session, search: str, value: str) -> List[AppraisalSectionSchema]:
    #     pass

    # def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
    #     return appraisal_section_repo.get_by_kwargs(self, db, kwargs)


login_service = LoginService()