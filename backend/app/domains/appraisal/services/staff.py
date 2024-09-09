from domains.appraisal.respository.staff import Staff_form_actions as Staff_form_repo
from domains.appraisal.schemas.staff import StaffSchema, StaffUpdate, StaffCreate
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




class StaffService:


    def list_staff(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[StaffSchema]:
        staff = Staff_form_repo.get_all(db=db, skip=skip, limit=limit)
        return staff

    async def create_staff(self, *, db: Session, staff: StaffCreate) -> StaffSchema:

        
        #check for duplicate email entries in staff table
        check_email = db.query(Staff).filter(Staff.email ==staff.email).first()
        if check_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email already exist")


        #check if department_id exists in department table 
        check_department_id = db.query(Department).filter(Department.id ==staff.department_id).first()
        if not check_department_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
        

        check_if_role_id_exists = db.query(Role).filter(Role.id == staff.role_id).first()
        if not check_if_role_id_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role does not exist")


        check_if_user_email_exists = db.query(User).filter(User.email == staff.email).first()
        if check_if_user_email_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="staff with email %s already exists" % staff.email)
        

        staff_obj = await Staff_form_repo.create(db=db, obj_in=staff)

        user_in = User()
        user_in.email = staff.email
        user_in.reset_password_token = None
        user_in.staff_id = staff_obj.id
        user_in.role_id = staff.role_id
        db.add(user_in)
        db.commit()
        db.refresh(user_in)

        ## if staff is created successfully 
        ## send an email to reset the password 
        ## confirm user email 
    # user = db.query(User).filter(User.email == reset_password_request.email).first()

    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    
    # Generate reset token

        token = password_reset_service.generate_reset_token()
        user_in.reset_password_token  = token
        # user.reset_password_token = token
        db.commit()

        # Send email with the reset link
        reset_link = f"{settings.FRONTEND_URL}/login/resetpassword?token={token}"
        
        # For demo purposes, print the reset link (use an email sender in production)
        # print(f"Reset link: {reset_link}")
        # print(f"User Emaail: {user.email}")
        
        # In production, send email with aiosmtplib or any other email library
        email_data = await send_reset_email(staff.email, reset_link)

        # print(f"email_data: {email_data}")

        await Email.sendMailService(email_data, template_name='password_reset.html')
        
        JSONResponse(content={"message": "Password reset link has been sent to your email."}, status_code=200)


        return staff_obj
    
    

    def update_staff(self, *, db: Session, id: UUID, staff: StaffUpdate) -> StaffSchema:
        get_staff1 = Staff_form_repo.get(db=db, id=id)
        if not get_staff1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        update_staff = Staff_form_repo.update(db=db, db_obj=get_staff1, obj_in=staff)
        return update_staff
 

    def get_staff(self, *, db: Session, id: UUID) -> StaffSchema:
        get_staff = Staff_form_repo.get(db=db, id=id)
        if not get_staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
        return get_staff

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

    def search_staff(self, *, db: Session, search: str, value: str) -> List[StaffSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return Staff_form_repo.get_by_kwargs(self, db, kwargs)


staff_service = StaffService()