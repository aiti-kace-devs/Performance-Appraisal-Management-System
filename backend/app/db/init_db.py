from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4
from sqlalchemy import func 
# from domains.appraisal.models.roles import Role
# from domains.appraisal.models.permissions import Permission
from domains.appraisal.models.role_permissions import Role, Permission
from uuid import uuid4


SUPER_ADMIN_NAME: str = "Super Admin"
SUPER_ADMIN_PHONE_NUMBER: str = "9876543210"
SUPER_ADMIN_EMAIL: str = "superadmin@admin.com"
SUPER_ADMIN_PASSWORD: str = "openforme"
SUPER_ADMIN_ROLE: str = "super_admin"
SUPER_ADMIN_STATUS: bool = True


def init_db(db: Session):
    ## check if a super admin does not exitst and create super admin

    # Check if the super_admin role already exists
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

    # if db.query(func.count(Role.id)).scalar() == 0: 
            

    #         payload = RolePermissionCreate(
    #         name="super_admin",
    #         permissions=[{"name": "create"}, {"name": "read"}, {"name": "update"}, {"name": "delete"}]
    #     )
            
            
    # # role_perm_service.create_role_perm(role_perm=payload, db=db)
    #         actions.create_role_perm(role_perm=payload, db=db)

    # return {"detail": "Roles and permissions initialized"}


    # # Create 1st Superuser
    # admin = userCRUD.get_by_email(db=db, email=SUPER_ADMIN_EMAIL)

    # ## check if the Role Table is empty before inserting 

    # if db.query(func.count(Role.id)).scalar() == 0: 
        
    #     ## create the first role and permission in the system for admin 

    #     payload = schema.CreateRolePerm(
    #         name="super_admin",
    #         permissions=[{"name": "create"}, {"name": "read"}, {"name": "update"}, {"name": "delete"}]
    #     )

    #     rolePermBaseActions.create_roles_perm(obj_in=payload, db=db)

    #     payload_admin = schema.CreateRolePerm(
    #         name="admin",
    #         permissions = [{"name": "create"}, {"name": "read"}]
    #     )

    #     rolePermBaseActions.create_roles_perm(obj_in=payload_admin, db=db)

    #     payload_moderator = schema.CreateRolePerm(
    #          name="moderator",
    #          permissions = [{"name": "read"}]
    #     )

    #     rolePermBaseActions.create_roles_perm(obj_in=payload_moderator, db=db)

    #     payload_moderator = schema.CreateRolePerm(
    #          name="user",
    #          permissions = [{"name": "none"}]
    #     )

    #     rolePermBaseActions.create_roles_perm(obj_in=payload_moderator, db=db)
    #     ## get the role_id of that permission and assign it to the admin upon creation

       
    # ## querying the role table to return the first role and assign it to 
    # ## super admin 
    # role = db.query(Role).filter(Role.name == "super_admin").first()

    # if admin:
    #     db.query(User).filter(User.id == admin.id, User.email == SUPER_ADMIN_EMAIL).update({
    #             User.role_id: role.id
    #         },synchronize_session=False)
    #     db.flush()
    #     db.commit()

    # admin_in = schema.CreateUser(
    #     name=SUPER_ADMIN_NAME,
    #     contact=SUPER_ADMIN_PHONE_NUMBER,
    #     email=SUPER_ADMIN_EMAIL,
    #     password=SUPER_ADMIN_PASSWORD,
    #     is_active=SUPER_ADMIN_STATUS,
    #     reset_password_token=None,
    #     role_id=role.id
    # )
    # userBaseActions.create_super_admin(obj_in = admin_in, db = db)
