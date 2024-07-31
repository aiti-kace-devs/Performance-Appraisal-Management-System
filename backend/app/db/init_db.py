from aiohttp import Payload
from sqlalchemy.orm import Session
from pydantic import UUID4, ValidationError
from sqlalchemy import func 
from domains.appraisal.models.users import User
from domains.appraisal.schemas.users import UserCreate



SUPER_ADMIN_NAME: str = "Super Admin"
SUPER_ADMIN_PHONE_NUMBER: str = "9876543210"
SUPER_ADMIN_EMAIL: str = "superadmin@admin.com"
SUPER_ADMIN_PASSWORD: str = "openforme"
SUPER_ADMIN_ROLE: str = "super_admin"
SUPER_ADMIN_STATUS: bool = True


def init_db(db: Session) -> None:
     
    



   #   payload = {

   #        "email":"abc@gmail.com",
   #        "password" : "eeeee552d93",
   #        "reset_password_token" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNzIyMDA1Mjk5LCJleHAiOjE3MjIwMDcwOTl9.dsuVb4EELOcI-ECkqHWrYOdXiUeBrJxRP_09DR1a0Zs",
   #        "role_id":"03e8beaa-ba9f-4192-b788-ffcff2cef500",
   #        "staff_id":"03e8beaa-ba9f-4192-b788-ffcff2cef705"
   #        }
     

   #   try:
   #      data = UserCreate(**payload)
   #      print("data :", data)
   #      db_add = User(**payload)  #model class name
   #      db.add(db_add)
   #      db.commit()
   #      db.refresh(db_add)
   #      print("Data inserted Successfully")
   #   except ValidationError as e:
   #      print(e.json())

     


   

    return False

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
