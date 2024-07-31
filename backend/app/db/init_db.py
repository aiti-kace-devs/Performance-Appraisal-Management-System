from aiohttp import Payload
from sqlalchemy.orm import Session
from pydantic import UUID4, ValidationError
from sqlalchemy import func 
# from domains.appraisal.models.appraisal_submission import AppraisalSubmission
# from domains.appraisal.schemas.appraisal_submission import AppraisalSubmissionCreate



SUPER_ADMIN_NAME: str = "Super Admin"
SUPER_ADMIN_PHONE_NUMBER: str = "9876543210"
SUPER_ADMIN_EMAIL: str = "superadmin@admin.com"
SUPER_ADMIN_PASSWORD: str = "openforme"
SUPER_ADMIN_ROLE: str = "super_admin"
SUPER_ADMIN_STATUS: bool = True


def init_db(db: Session) -> None:

    # payload = {
    #     "appraisals_id" : "03e8beaa-ba9f-4192-b788-ffcff2cef925",
    #     "staffs_id" : "03e8beaa-ba9f-4192-b788-ffcff2cef965",
    #     "appraisal_forms_id" : "03e8beaa-ba9f-4192-b788-ffcff2cef972",
    #     "submitted_values" : {"homework": "well done"},
    #     "started_at" : None,
    #     "completed_at" : None,
    #     "approval_date" : None,
    #     "submitted" : True,
    #     "completed" : True,
    #     "approval_status" : False,
    #     "comment" : "Well done on completing your work"

    # }


    # try:
    #     db_add = AppraisalSubmissionCreate(**payload)  #model class name
    #     print("db_add", db_add)
    #     add = AppraisalSubmission(**payload)
    #     db.add(add)
    #     db.commit()
    #     db.refresh(add)
    #     print("Data inserted Successfully")
    # except ValidationError as e:
    #     print(e.json())

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
