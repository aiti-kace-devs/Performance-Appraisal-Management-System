from domains.auth.services.user_account import users_forms_service as actions
from domains.auth.schemas import user_account as userSchema
from domains.auth.respository.user_account import users_form_actions
from domains.auth.services.password_reset import password_reset_service
from domains.auth.schemas.password_reset import ResetPasswordRequest
from services.email_service import EmailSchema,Email 
from domains.auth.models.users import User
from fastapi.responses import JSONResponse
from config.settings import settings
from typing import Any, List
from fastapi import APIRouter, Depends,status
from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from domains.appraisal.models.staff_role_permissions import Role, Staff
from domains.auth.schemas import user_account as schemas

from db.session import get_db


users_router = APIRouter(
       prefix="/users",
    tags=["Users Account"],
    responses={404: {"description": "Not found"}},
)





@users_router.get(
    "/all",
    response_model=List[schemas.UserSchema]
)
def list_users(
        db: Session = Depends(get_db),

        skip: int = 0,
        limit: int = 100
) -> Any:
    users_router = actions.list_users_forms(db=db, skip=skip, limit=limit)
    return users_router




@users_router.put(
    "/{id}",
    response_model=schemas.UserSchema
)
def update_users(
        *, db: Session = Depends(get_db),

        id: UUID4,
        users_forms_in: schemas.UserUpdate,
) -> Any:
    users_router = actions.get_user_by_id(db=db, id=id)
    if not users_router:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="users_forms_router not found"
        )
    users_router = actions.update_users_forms(db=db, id=users_router.id, users_form=users_forms_in)
    return users_router





@users_router.get(
    "/{id}",
    response_model=schemas.UserSchema
)
def get_user_by_id(
        *, db: Session = Depends(get_db),

        id: UUID4
) -> Any:
    get_user = actions.get_user_by_id(db=db, id=id)
    if not get_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return get_user



async def send_reset_email(email: str, reset_link: str) -> EmailSchema:
    ## prepare the email data
    email_data = EmailSchema(
        subject= "Password Reset Request",
        email=  [email],
        body= {
            "name": email, 
            "reset_link": reset_link,
            "app_name": "Appraisal Management System"
        }
    )

    return email_data





@users_router.get("/forgot-password/{email}")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = password_reset_service.generate_reset_token()
    user.reset_password_token = token
    db.commit()

    try:

        reset_link = f"{settings.FRONTEND_URL}/login/resetpassword?token={token}"
        email_data = await send_reset_email(user.email, reset_link)
        await Email.sendMailService(email_data, template_name='password_reset.html')
        
    except Exception as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='There was an error sending email')
    
    return JSONResponse(content={"message": "Password reset link has been sent to your email."}, status_code=200)







@users_router.put("/reset-password-token/{token}", response_model=userSchema.UserSchema)
async def update_user_with_reset_password_token(*, db: Session = Depends(get_db), token: str, obj_in: userSchema.UpdatePassword):
    update_user = users_form_actions.get_by_reset_password_token(db=db, token=token)
    if not update_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Token")

    data = users_form_actions.update_user_after_reset_password(db=db, db_obj=update_user, obj_in=obj_in)
    db.refresh(data)

    user = (
        db.query(User)
        .join(Staff, User.staff_id == Staff.id)
        .join(Role, User.role_id == Role.id)
        .filter(User.id == data.id)
        .first()
    )
        
    
    user_data = {
        "id": user.id,
        "is_active": user.is_active,
        "failed_login_attempts": user.failed_login_attempts,
        "account_locked_until": user.account_locked_until,
        "lock_count": user.lock_count,
        "email": user.email,
        "password": user.password,
        "reset_password_token": user.reset_password_token,
        "staff": {
            "id": user.staffs[0].id if user.staffs else None, 
            "first_name": user.staffs[0].first_name if user.staffs else None,
            "last_name": user.staffs[0].last_name if user.staffs else None,
            "other_name": user.staffs[0].other_name if user.staffs else None,
            "full_name": f"{user.staffs[0].first_name} {user.staffs[0].last_name}" + (f" {user.staffs[0].other_name}" if user.staffs[0].other_name or user.staffs[0].first_name or user.staffs[0].other_name else None)
        } if user.staffs else None, 
        "role": {
            "id": user.roles[0].id if user.roles else None, 
            "name": user.roles[0].name if user.roles else None,
        } if user.roles else None, 
    }


    return user_data