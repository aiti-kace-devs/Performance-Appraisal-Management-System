from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4
from sqlalchemy import func 
from domains.appraisal.models.roles import Role



SUPER_ADMIN_NAME: str = "Super Admin"
SUPER_ADMIN_PHONE_NUMBER: str = "9876543210"
SUPER_ADMIN_EMAIL: str = "superadmin@admin.com"
SUPER_ADMIN_PASSWORD: str = "openforme"
SUPER_ADMIN_ROLE: str = "super_admin"
SUPER_ADMIN_STATUS: bool = True


def init_db(db: Session) -> None:
    ## check if a super admin does not exitst and create super admin

    ## check if the Role Table is empty before inserting 

    if db.query(func.count(Role.id)).scalar() == 0: 

        roles_to_create = ["super_admin", "HR", "Supervisor", "Staff"]
        permissions_to_create = ["read", "write"]

        # created_permissions = {}
        # for perm_name in permissions_to_create:
        #     permission = db.query(Permission).filter(Permission.name == perm_name).first()
        #     if not permission:
        #         permission = Permission(name=perm_name)
        #         db.add(permission)
        #         db.commit()
        #         db.refresh(permission)
        #     created_permissions[perm_name] = permission

        for role_name in roles_to_create:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name)
                # if role_name == "super_admin":
                #     role.permissions = list(created_permissions.values())
                db.add(role)
                db.commit()
                db.refresh(role)

    # return {"detail": "Roles and permissions initialized"}
    return {"detail": "Roles initialized"}

    
    
   
        # raise HTTPException(status_code=400, detail="Super Admin role already exists")
    
    # read_permission = db.query(Permission).filter(Permission.name == "read").first()
    # if not read_permission:
    #     read_permission = Permission(name="read")
    #     db.add(read_permission)
    #     db.commit()
    #     db.refresh(read_permission)
    
    # write_permission = db.query(Permission).filter(Permission.name == "write").first()
    # if not write_permission:
    #     write_permission = Permission(name="write")
    #     db.add(write_permission)
    #     db.commit()
    #     db.refresh(write_permission)

    # admin_role = Role(name="admin", permissions=[read_permission, write_permission])
    super_admin_role = Role(name="super_admin")
    db.add(super_admin_role)

    db.commit()
    db.refresh(super_admin_role)
    # return {"detail": "Admin role with read and write permissions created"}
    return {"detail": "Admin role with read and write permissions created"}

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
