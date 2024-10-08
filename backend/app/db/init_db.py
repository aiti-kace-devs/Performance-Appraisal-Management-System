from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4, ValidationError
from sqlalchemy import func
from pydantic import UUID4
from sqlalchemy import func 
# from domains.appraisal.models.roles import Role
# from domains.appraisal.models.permissions import Permission
from domains.appraisal.models.role_permissions import Role, Permission
from uuid import uuid4
from domains.auth.respository.user_account import users_form_actions
from domains.auth.models.users import User
from domains.auth.schemas.user_account import UserCreate

SUPER_ADMIN_NAME: str = "Super Admin"
SUPER_ADMIN_PHONE_NUMBER: str = "9876543210"
SUPER_ADMIN_EMAIL: str = "superadmin@admin.com"
SUPER_ADMIN_PASSWORD: str = "openforme"
SUPER_ADMIN_ROLE: str = "super_admin"
SUPER_ADMIN_STATUS: bool = True


def init_db(db: Session):
    ## check if a super admin does not exitst and create super admin

    # # Check if the super_admin role already exists
    super_admin_role = db.query(Role).filter(Role.name == "super_admin").first()
    if super_admin_role:
        return  # super_admin role already exists, no need to initialize

    # Create the super_admin role
    super_admin_role = Role(id=uuid4(), name="super_admin")
    db.add(super_admin_role)
    db.commit()

    # Define the required permissions
    permission_names = ["read", "create", "write", "update", "delete", "approve"]

    # Create and assign the permissions to the super_admin role
    for perm_name in permission_names:
        permission = db.query(Permission).filter(Permission.name == perm_name).first()
        if not permission:
            permission = Permission(id=uuid4(), name=perm_name)
            db.add(permission)
            db.commit()
        
        # Add permission to the role
        super_admin_role.permissions.append(permission)

    db.commit()





from utils.security import pwd_context


def create_super_admin(db: Session):

    # Create 1st Superuser
    admin = db.query(User).filter(User.email == "superadmin@admin.com").first()       

    role = db.query(Role).filter(Role.name == "super_admin").first()

    if admin:
        return
        
    else:
        admin_in = User(
        email=SUPER_ADMIN_EMAIL,
        password=pwd_context.hash(SUPER_ADMIN_PASSWORD),
        reset_password_token=None,
        staff_id=uuid4(),
        role_id=role.id
        )
        db.add(admin_in)
        db.commit()
        db.refresh(admin_in)
