from domains.appraisal.respository.staff import Staff_form_actions as Staff_form_repo
from domains.appraisal.schemas.staff import StaffSchema,StaffUpdate,StaffCreate,StaffWithFullNameInDBBase,DepartmentInfo,RoleInfo
from domains.appraisal.models.staff_role_permissions import Role, Staff, staff_permissions
from domains.appraisal.schemas.staff import StaffSchema, StaffUpdate, StaffCreate, StaffResponse
from domains.appraisal.models.department import Department
# from domains.appraisal.models.staff import Staff
from domains.auth.models.users import User
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from db.base_class import UUID
from typing import List, Any
from config.settings import settings
from domains.auth.schemas.password_reset import ResetPasswordRequest
from domains.auth.services.password_reset import password_reset_service
from fastapi.responses import JSONResponse
from services.email_service import EmailSchema, Email
from domains.auth.apis.login import send_reset_email
from sqlalchemy.exc import SQLAlchemyError
from domains.appraisal.models.staff_role_permissions import Staff
from domains.appraisal.respository.department import department_actions
from domains.appraisal.respository.role import role_actions
from domains.auth.respository.user_account import users_form_actions
import re

class StaffService:


    async def list_staff(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffWithFullNameInDBBase]:

        staff_query = (
            db.query(Staff, Department.id.label('department_id'), Department.name.label('department_name'), Role.id.label('role_id'), Role.name.label('role_name'))
            .join(Department, Staff.department_id == Department.id)
            .join(User, User.staff_id == Staff.id)
            .join(Role, User.role_id == Role.id)
            .offset(skip)
            .limit(limit)
        )
        
        staff_with_details = staff_query.all()
        
        staff_list = [
            StaffWithFullNameInDBBase(
                id=staff.id,
                title=staff.title,
                first_name=staff.first_name,
                last_name=staff.last_name,
                other_name=staff.other_name,
                full_name=f"{staff.first_name} {staff.last_name}" + (f" {staff.other_name}" if staff.other_name else ""),
                gender=staff.gender,
                email=staff.email,
                position=staff.position,
                grade=staff.grade,
                appointment_date=staff.appointment_date,
                department_id=DepartmentInfo(
                    id=department_id,
                    name=department_name
                ),
                role_id=RoleInfo(
                    id=role_id,
                    name=role_name
                )
            )
            for staff, department_id, department_name, role_id, role_name in staff_with_details
        ]

        
        return staff_list


    



    async def create_staff(self, *, db: Session, staff: StaffCreate):

        #check for duplicate email entries in staff table
        check_email = Staff_form_repo.get_by_email(db, staff.email)
        if check_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff with email %s already exists" % staff.email)


        #check if department_id exists in department table 
        check_department_id = department_actions.get(db, staff.department_id)
        if not check_department_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
        

        check_if_role_id_exists = role_actions.get(db, staff.role_id)
        if not check_if_role_id_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role does not exist")


        check_if_user_email_exists = users_form_actions.get_by_email(db, staff.email)
        if check_if_user_email_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with email %s already exists" % staff.email)
        
        ## Check for permissions associated with the role 
        role = db.query(Role).filter(Role.id == staff.role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permissions for this role not found")

        staff_data = staff.dict()
        staff_data['role_id'] = staff.role_id
        
        staff_obj = await Staff_form_repo.create(db=db, obj_in=StaffCreate(**staff_data))
        
        user_in = User()
        user_in.email = staff.email
        user_in.reset_password_token = None
        user_in.staff_id = staff_obj.id
        user_in.role_id = staff.role_id
        db.add(user_in)
        db.commit()
        db.refresh(user_in)


        # db.commit()
        permissions_ids = [] # List to hold permission IDs
        # Assign permissions based on the role
        for permission in role.permissions:  
            staff_permission = {
                "staff_id": staff_obj.id,
                "permission_id": permission.id
            }
            db.execute(staff_permissions.insert().values(staff_permission))
            permissions_ids.append(permission.id)

        db.commit()


        token = password_reset_service.generate_reset_token()
        user_in.reset_password_token  = token
        # user.reset_password_token = token
        db.commit()

        # Send email with the reset link
        reset_link = f"{settings.FRONTEND_URL}/login/resetpassword?token={token}"

        # email_data = await send_reset_email(staff.email, reset_link)

        # await Email.sendMailService(email_data, template_name='password_reset.html')
        
        JSONResponse(content={"message": "Password reset link has been sent to your email."}, status_code=200)

        data = {
            'id': staff_obj.id,
            'title': staff_obj.title,
            'first_name': staff_obj.first_name,
            'last_name': staff_obj.last_name,
            'other_name': staff_obj.other_name,
            'full_name': f"{staff_obj.first_name} {staff_obj.last_name}" + (f" {staff_obj.other_name}" if staff_obj.other_name else ""),
            'department_id': {
                'id': check_department_id.id,
                'name': check_department_id.name,
            },
            'gender': staff_obj.gender,
            'email': staff_obj.email,
            'position': staff_obj.position,
            'grade': staff_obj.grade,
            'appointment_date': staff_obj.appointment_date, 
            'role_id': {
                "id": check_if_role_id_exists.id,
                "name": check_if_role_id_exists.name,
            },
            'permissions_ids': permissions_ids,
            'created_at': staff_obj.created_date,
        }

        return data
    
    

    def update_staff(self, *, db: Session, id: UUID, staff: StaffUpdate):
        get_staff1 = Staff_form_repo.get(db=db, id=id)

        get_staff_user = db.query(User).filter(User.staff_id == get_staff1.id).first()
        if not get_staff1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        Staff_form_repo.update(db=db, db_obj=get_staff1, obj_in=staff)


        get_staff_department = department_actions.get(db, get_staff1.department_id)

        get_staff_user.role_id = staff.role_id
        db.commit()
        get_staff_role = role_actions.get(db, staff.role_id)
        
        db.refresh(get_staff_role)
        
        data = {
            'id': get_staff1.id,
            'title': get_staff1.title,
            'first_name': get_staff1.first_name,
            'last_name': get_staff1.last_name,
            'other_name': get_staff1.other_name,
            'full_name': f"{get_staff1.first_name} {get_staff1.last_name}" + (f" {get_staff1.other_name}" if get_staff1.other_name else ""),
            'department_id': {
                'id': get_staff_department.id,
                'name': get_staff_department.name,
            },
            'gender': get_staff1.gender,
            'email': get_staff1.email,
            'position': get_staff1.position,
            'grade': get_staff1.grade,
            'appointment_date': get_staff1.appointment_date, 
            'role_id': {
                'id': get_staff_role.id,
                'name': get_staff_role.name,
            },          
            'created_at': get_staff1.created_date,
        }

        return data
        

    






    def delete_staff(self, *, db: Session, id: UUID):
        get_staff2 = Staff_form_repo.get(db=db, id=id)
        if not get_staff2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        Staff_form_repo.remove(db=db, id=id)
        

        get_staff_department = department_actions.get(db, get_staff2.department_id)
        
        data = {
            'id': get_staff2.id,
            'title': get_staff2.title,
            'first_name': get_staff2.first_name,
            'last_name': get_staff2.last_name,
            'other_name': get_staff2.other_name,
            'full_name': f"{get_staff2.first_name} {get_staff2.last_name}" + (f" {get_staff2.other_name}" if get_staff2.other_name else ""),
            'department_id': get_staff_department.name,
            'gender': get_staff2.gender,
            'email': get_staff2.email,
            'position': get_staff2.position,
            'grade': get_staff2.grade,
            'appointment_date': get_staff2.appointment_date,           
            'created_at': get_staff2.created_date,
        }

        return data
    







    def get_staff_by_id(self, *, db: Session, id: UUID):
        get_staff_by_id = Staff_form_repo.get(db, id)
        if not get_staff_by_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="staff not found"
            )
        
        get_staff_department = department_actions.get(db, get_staff_by_id.department_id)
        get_staff_user = db.query(User).filter(User.staff_id == get_staff_by_id.id).first()
        get_staff_role = role_actions.get(db, get_staff_user.role_id)
        
        data = {
            'id': get_staff_by_id.id,
            'title': get_staff_by_id.title,
            'first_name': get_staff_by_id.first_name,
            'last_name': get_staff_by_id.last_name,
            'other_name': get_staff_by_id.other_name,
            'full_name': f"{get_staff_by_id.first_name} {get_staff_by_id.last_name}" + (f" {get_staff_by_id.other_name}" if get_staff_by_id.other_name else ""),
            'department_id': {
                'id': get_staff_department.id,
                'name': get_staff_department.name,
            },
            'gender': get_staff_by_id.gender,
            'email': get_staff_by_id.email,
            'position': get_staff_by_id.position,
            'grade': get_staff_by_id.grade,
            'appointment_date': get_staff_by_id.appointment_date, 
            'role_id': {
                'id': get_staff_role.id,
                'name': get_staff_role.name,
            },          
            'created_at': get_staff_by_id.created_date,
        }

        return data

    def get_staff_by_keywords(self, *, db: Session, tag: str) -> List[StaffSchema]:
        pass




    def search_staff(self, db: Session, name: str):
        search_fields = ['first_name', 'last_name', 'other_name']
        response = None

        search_value = re.sub(r'[^\w\s]', '', name.strip())  # Remove special characters
        if not search_value:
            return response

        try:
            for field in search_fields:
                if hasattr(Staff, field):
                    response = db.query(Staff).filter(
                        getattr(Staff, field).ilike(f"%{search_value}%")
                    ).first()
                    if response:
                        response = response.to_dict()  # Convert the model instance to a dictionary
                        break

        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            return {"error": "An error occurred while processing your request."}
        except KeyError as ke:
            print(f"Key error: {ke}")
            return {"error": "Invalid search parameter."}
        
        return response




    def get_supervisors(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffWithFullNameInDBBase]:
        get_supervisor = db.query(Role).filter(Role.name == "Supervisor").first()

        if not get_supervisor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supervisor role not found")

        staff_query = (
            db.query(Staff, Department.name)
            .join(Department, Staff.department_id == Department.id)
            .join(User, User.staff_id == Staff.id)  # Separate join for User
            .filter(User.role_id == get_supervisor.id)  # Filter by role_id
            .offset(skip)
            .limit(limit)
        )

        staff_with_department = staff_query.all()

        # Create StaffWithFullNameInDBBase instances
        staff_list = [
            StaffWithFullNameInDBBase(
                id=staff.id,
                title=staff.title,
                first_name=staff.first_name,
                last_name=staff.last_name,
                other_name=staff.other_name,
                full_name=f"{staff.first_name} {staff.last_name}" + (f" {staff.other_name}" if staff.other_name else ""),
                gender=staff.gender,
                email=staff.email,
                position=staff.position,
                grade=staff.grade,
                appointment_date=staff.appointment_date,
                department_id=department_name
            )
            for staff, department_name in staff_with_department
        ]

        return staff_list





    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return Staff_form_repo.get_by_kwargs(self, db, kwargs)


staff_service = StaffService()