from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.base_class import UUID
from domains.auth.respository.user_account import users_form_actions as users_form_repo
from domains.auth.schemas.user_account import UserSchema, UserCreate, UserUpdate,UpdatePassword
from domains.auth.models.users import User
from domains.appraisal.models.staff_role_permissions import Role, Staff

class UserService:


    def list_users_forms(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[UserSchema]:
        users = (
            db.query(User)
            .join(Staff, User.staff_id == Staff.id)
            .join(Role, User.role_id == Role.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        
        user_list = []
        for user in users:

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

            user_list.append(user_data)

        return user_list
    




    def get_user_by_id(self, *, db: Session, id: UUID) -> UserSchema:
        get_user = users_form_repo.get(db=db, id=id)
        if not get_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="users_form not found")
        

        user = (
        db.query(User)
        .join(Staff, User.staff_id == Staff.id)
        .join(Role, User.role_id == Role.id)
        .filter(User.id == get_user.id)
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




    def create_users_forms(self, *, db: Session, users_form: UserCreate) -> UserSchema:
        users_form = users_form_repo.create(db=db, obj_in=users_form)
        return users_form

    def update_users_forms(self, *, db: Session, id: UUID, users_form: UserUpdate) -> UserSchema:
        users_form_ = users_form_repo.get(db=db, id=id)
        if not users_form_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="users_form not found")
        users_form_ = users_form_repo.update(db=db, db_obj=users_form_, obj_in=users_form)
        return users_form_



    def delete_users_forms(self, *, db: Session, id: UUID) -> UserSchema:
        users_form = users_form_repo.get(db=db, id=id)
        if not users_form:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="users_form not found")
        users_form = users_form_repo.remove(db=db, id=id)
        return users_form

    def get_users_forms_by_id(self, *, id: UUID) -> UserSchema:
        users_form = users_form_repo.get(id)
        if not users_form:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="users_form not found"
            )
        return users_form



users_forms_service = UserService()