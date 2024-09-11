from domains.appraisal.respository.staff import Staff_form_actions as Staff_form_repo
from domains.appraisal.schemas.staff import StaffSchema,StaffUpdate,StaffCreate,StaffWithFullNameInDBBase
from domains.appraisal.models.role_permissions import Role
from domains.appraisal.models.department import Department
from domains.appraisal.models.staff import Staff
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
from domains.appraisal.models.staff import Staff
from domains.appraisal.respository.department import department_actions
from domains.appraisal.respository.role import role_actions
from domains.auth.respository.user_account import users_form_actions
import re

class StaffService:


    async def list_staff(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffWithFullNameInDBBase]:
        # Query to get staff and their department names
        staff_query = db.query(Staff, Department.name).join(Department, Staff.department_id == Department.id).offset(skip).limit(limit)
        
        # Fetch results
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
        

        staff_obj = await Staff_form_repo.create(db=db, obj_in=staff)

        user_in = User()
        user_in.email = staff.email
        user_in.reset_password_token = None
        user_in.staff_id = staff_obj.id
        user_in.role_id = staff.role_id
        db.add(user_in)
        db.commit()
        db.refresh(user_in)

        token = password_reset_service.generate_reset_token()
        user_in.reset_password_token  = token
        # user.reset_password_token = token
        db.commit()

        # Send email with the reset link
        reset_link = f"{settings.FRONTEND_URL}/login/resetpassword?token={token}"

        email_data = await send_reset_email(staff.email, reset_link)

        await Email.sendMailService(email_data, template_name='password_reset.html')
        
        JSONResponse(content={"message": "Password reset link has been sent to your email."}, status_code=200)


        data = {
            'id': staff_obj.id,
            'title': staff_obj.title,
            'first_name': staff_obj.first_name,
            'last_name': staff_obj.last_name,
            'other_name': staff_obj.other_name,
            'department_id': {
                "id": check_department_id.id,
                "name": check_department_id.name
            }, 
            'gender': staff_obj.gender,
            'email': staff_obj.email,
            'position': staff_obj.position,
            'grade': staff_obj.grade,
            'appointment_date': staff_obj.appointment_date,           
            'role_id': {
                "id": check_if_role_id_exists.id,
                "name": check_if_role_id_exists.name
            },
            'created_at': staff_obj.created_date,
        }

        return data
    
    

    def update_staff(self, *, db: Session, id: UUID, staff: StaffUpdate) -> StaffSchema:
        get_staff1 = Staff_form_repo.get(db=db, id=id)
        if not get_staff1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        update_staff = Staff_form_repo.update(db=db, db_obj=get_staff1, obj_in=staff)
        return update_staff
 

    def get_staff(self, *, db: Session, id: UUID):
        get_staff = Staff_form_repo.get(db=db, id=id)
        if not get_staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        
        get_staff_department = department_actions.get(db, get_staff.department_id)
        get_user = db.query(User).filter(User.staff_id == get_staff.id).first()
        get_staff_role = role_actions.get(db, get_user.role_id)
        
        data = {
            'id': get_staff.id,
            'title': get_staff.title,
            'first_name': get_staff.first_name,
            'last_name': get_staff.last_name,
            'other_name': get_staff.other_name,
            'full_name': f"{get_staff.first_name} {get_staff.last_name}" + (f" {get_staff.other_name}" if get_staff.other_name else ""),
            'department_id': {
                "id": get_staff_department.id,
                "name": get_staff_department.name
            }, 
            'gender': get_staff.gender,
            'email': get_staff.email,
            'position': get_staff.position,
            'grade': get_staff.grade,
            'appointment_date': get_staff.appointment_date,           
            'role_id': {
                "id": get_staff_role.id,
                "name": get_staff_role.name
            },
            'created_at': get_staff.created_date,
        }

        return data



    def delete_staff(self, *, db: Session, id: UUID) -> StaffSchema:
        get_staff2 = Staff_form_repo.get(db=db, id=id)
        if not get_staff2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        delete_staff = Staff_form_repo.remove(db=db, id=id)
        return delete_staff

    def get_staff_by_id(self, *, id: UUID) -> StaffSchema:
        get_staff_by_id = Staff_form_repo.get(id)
        if not get_staff_by_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="staff not found"
            )
        return get_staff_by_id

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




    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return Staff_form_repo.get_by_kwargs(self, db, kwargs)


staff_service = StaffService()