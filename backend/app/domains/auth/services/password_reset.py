from fastapi.response import JSONResponse 
import random 
import string 

from fastapi import Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from db.session import get_db
from domains.auth.models.users import User
from domains.auth.schemas.password_reset import ReResetPasswordRequest

class PasswordResetService:

    def generate_reset_token(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    
    def get_current_user_email(self, request: Request, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.email == email).first() 

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    

password_reset_service = PasswordResetService