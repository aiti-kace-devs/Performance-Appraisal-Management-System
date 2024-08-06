# from typing import List, Any
# from fastapi import HTTPException, status
# from sqlalchemy.orm import Session


# from db.base_class import UUID
# from domains.appraisal.respository.role_permission import role_perm_actions as role_perm_repo
# from domains.appraisal.schemas.role_permissions import RolePermissionCreate, RolePermissionUpdate, RolePermission



# class RolePermssionService:
#      ## function to get role
#     def get_role_perm(self, db:Session, role_id: UUID):
#         role_perm = role_perm_repo.get(db, id=role_id)   
#         return role_perm 
#     ## functions to get all roles 
#     def get_all_roles_perm(self, db:Session, skip: int = 0, limit: int = 10):
#         role_perms = role_perm_repo.get_all(db=db, skip=skip, limit=limit)
#         return role_perms
    
#     ## function to define new roles  in the system..
#     # def create_role_perm(self, *, role_perm: RolePermissionCreate, db:Session):

#     #     # Check if the role name already exists
#     #     existing_role = db.query(Role).filter(Role.name == role_perm.name).first()
        
#     #     if existing_role:
#     #         raise HTTPException(
#     #             status_code=status.HTTP_400_BAD_REQUEST,
#     #             detail=f"Role '{role_perm.name}' already exists."
#     #         )

#     #     db_role = self.model(name=role_perm.name)
#     #     # obj_in_data = jsonable_encoder(obj_in, **kw)
#     #     # db_obj = self.model(**obj_in_data)
#     #     # print(db_role)
#     #     # print(obj_in)
#     #     for per in role_perm.permissions:
#     #         try:
#     #             db_permission = db.query(Permission).filter(Permission.name == per.name).first()
#     #             if not db_permission:
#     #                 db_permission = Permission(name=per.name)
#     #             db_role.permissions.append(db_permission)    
#     #         except Exception as e:
#     #             db.rollback()
#     #             raise HTTPException(
#     #                 status_code=status.HTTP_400_BAD_REQUEST,
#     #                 detail=f"Permission '{per.name}' already exists."
#     #             )

#     #     db.add(db_role)
#     #     db.commit()
#     #     db.refresh(db_role)
#     #     return db_role


#     # def update_role_perm(self, obj_in: UpdateSchemaType, db: Session, **kw):
#     #     db_role = db.query(self.model).filter(self.model.id == obj_in.role_id).first()
#     #     if not db_role:
#     #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        
#     #     db_role.name = obj_in.name
#     #     db_role.permissions = []
#     #     for perm in obj_in.permissions:
#     #         db_permission = db.query(Permission).filter(Permission.name == perm.name).first()
#     #         if not db_permission:
#     #             db_permission = Permission(name=perm.name)
#     #         db_role.permissions.append(db_permission)
#     #     db.commit()
#     #     db.refresh(db_role)
#     #     return db_role
    


# role_perm_service = RolePermssionService()