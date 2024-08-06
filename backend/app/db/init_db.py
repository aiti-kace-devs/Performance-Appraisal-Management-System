from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4
from sqlalchemy import func 
from domains.appraisal.models.roles import Role




# SUPER_ADMIN_NAME: str = "Super Admin"
# SUPER_ADMIN_PHONE_NUMBER: str = "9876543210"
# SUPER_ADMIN_EMAIL: str = "superadmin@admin.com"
# SUPER_ADMIN_PASSWORD: str = "openforme"
# SUPER_ADMIN_ROLE: str = "super_admin"
# SUPER_ADMIN_STATUS: bool = True


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

    # payload = {
    # "department_id": "03e8beaa-ba9f-4192-b788-ffcff2cef925",
    # "appraisal_section_id":"03e8beaa-ba9f-4192-b788-ffcff2cef900",
    # "supervisor_id" : "03e8beaa-ba9f-4192-b788-ffcff2cef910",
    # "focus_area" : [{}]
    # }


#     payload = {
#     "department_id": "03e8beaa-ba9f-4192-b788-ffcff2cef925",
#     "appraisal_section_id": "03e8beaa-ba9f-4192-b788-ffcff2cef900",
#     "supervisor_id": "03e8beaa-ba9f-4192-b788-ffcff2cef925",
#     "focus_area": [
#         {
#             "objective": "Grow research enterprise to attract funding",
#             "strategies": {
#                 "0": "Complete and deploy [1] eAsset/ [2] SmartConferencing/ [3]Appraisal/ [4]FrontOffice",
#                 "1": "Provide Software Quality Assurance services for three external software products",
#                 "2": "SQA Collaborations with NITA",
#                 "3": "Develop capacities in Web Application Security Testing",
#                 "4": "Complete the development and testing of KCAP and pilot in at least [10] schools",
#                 "5": "Assemble drone kits to implement an AI-based agriculture solution: [irrigation/ spraying/ etc…]",
#                 "7": [
#                     {
#                         "resaerch_area": {
#                             "0": "GraphQL",
#                             "1": "Web Assembly(Wasm)",
#                             "2": "Asterisk with CRBT",
#                             "3": "Laravel",
#                             "4": "API development using Python and further research into back-end and front-end technologies"
#                         },
#                         "Note": "This will result in developing a prototype and article write-up for publication by September 2024. Only group effort is allowed and all group member should be indicated in the KRA form"
#                     }
#                 ],
#                 "6:": "Complete research work on the GPS-based asset tracking system and product pilot in the centres vehicles"
#             },
#             "kpi": {
#                 "0": "",
#                 "1": "",
#                 "2": "",
#                 "3": ""
#             },
#             "target": {
#                 "0": 2,
#                 "1": 1,
#                 "2": "Yes"
#             },
#             "responsibilty": {
#                 "0": "SE Unit",
#                 "1": "SE Unit",
#                 "2": "IT Unit"
#             }
#         },
#         {
#             "objective": "Staff Development",
#             "strategies": "Upgrade the technical knowledge and skills of the R&I team",
#             "kpi": "Number of staff trained",
#             "target": 5,
#             "responsibilty": "Research and Innovation Director"
#         }
#     ]
# }

#     # payload = {
#     #     "departent_id": "03e8beaa-ba9f-4192-b788-ffcff2cef925",
#     #     "appraisal_section_id":"03e8beaa-ba9f-4192-b788-ffcff2cef900",
#     #     "supervisor_id": "03e8beaa-ba9f-4192-b788-ffcff2cef925",
#     #     "focus_areas": [
#     #         {
#     #             "objective": "Grow research enterprise to attract funding",
#     #             "strategies": {
#     #                 "0": "Complete and deploy [1] eAsset/ [2] SmartConferencing/ [3]Appraisal/ [4]FrontOffice",
#     #                 "1": "Provide Software Quality Assurance services for three external software products",
#     #                 "2": "SQA Collaborations with NITA",
#     #                 "3": "Develop capacities in Web Application Security Testing",
#     #                 "4": "Complete the development and testing of KCAP and pilot in at least [10] schools",
#     #                 "5": "Assemble drone kits to implement an AI-based agriculture solution: [irrigation/ spraying/ etc…]",
#     #                 "6:": "Complete research work on the GPS-based asset tracking system and productpilot in the centres vehicles",
#     #                 "7": [
#     #                         {
#     #                             "resaerch_area": {
#     #                                 "0": "GraphQL",
#     #                                 "1": "Web Assembly(Wasm)",
#     #                                 "2": "Asterisk with CRBT",
#     #                                 "3": "Laravel",
#     #                                 "4": "API development using Python and further research into back-end and front-end technologies"
#     #                             },
#     #                             "Note": " This will result in developing a prototype and article write-up for publication by September 2024. Only group effort is allowed and all group member should be indicated in the KRA form"
#     #                         }
#     #                     ]
#     #             },
#     #             "kpi": {
#     #                 "0": "",
#     #                 "1": "",
#     #                 "2": "",
#     #                 "3": ""
#     #             },
#     #             "target": {
#     #                 "0": 2,
#     #                 "1": 1,
#     #                 "2": "Yes"
#     #             },
#     #             "responsibilty": {
#     #                 "0": "SE Unit",
#     #                 "1": "SE Unit",
#     #                 "2": "IT Unit"
#     #             }
#     #         },

#     #         {
#     #             "objective": "Staff Development",
#     #             "strategies": "Upgrade the technical knowledge and skills of the R&I team",
#     #             "kpi": "Number of staff trained",
#     #             "target": 5,
#     #             "responsibilty": "Research and Innovation Director"
#     #         }
#     #     ]
#     # }
    

#     try:
#         db_add = KraBankBaseCreate(**payload)  #model class name
#         print("db_add", db_add)
#         add = KraBank(**payload)
#         db.add(add)
#         db.commit()
#         db.refresh(add)
#         print("Data inserted Successfully")
#     except ValidationError as e:
#         print(e.json())




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





