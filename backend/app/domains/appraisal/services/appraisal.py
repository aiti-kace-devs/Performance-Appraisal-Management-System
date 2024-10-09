from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.base_class import UUID
from domains.appraisal.respository.appraisal import appraisal_form_actions as appraisal_repo
from domains.appraisal.schemas.appraisal import AppraisalSchema, AppraisalUpdate, AppraisalCreate
from domains.appraisal.models.appraisal_cycle import AppraisalCycle
from domains.appraisal.models.staff_role_permissions import Staff
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.models.appraisal_submission import AppraisalSubmission
from domains.appraisal.models.appraisal_form import AppraisalForm
from domains.appraisal.models.staff_supervisor import StaffSupervisor
import json




class AppraisalService:





    def get_appraisal_by_id(self, db: Session, id: UUID):
        get_staff_empty_info = {}
        get_staff_appraisal_submission = []
        data = []

        get_staff_info = db.query(Staff).filter(Staff.id == id).first()

        if not get_staff_info:
            return {
                "staff_info": {},
                "data": []
            }

        get_staff_appraisal_submission = db.query(AppraisalSubmission).filter(AppraisalSubmission.submitted_by == id).all()

        for submission in get_staff_appraisal_submission:
            appraisal_form = db.query(AppraisalForm).filter(AppraisalForm.id == submission.appraisal_forms_id).first()

            if appraisal_form:
              
                appraisal_section = db.query(AppraisalSection).filter(AppraisalSection.id == appraisal_form.appraisal_sections_id).first()

                form_fields = json.loads(appraisal_form.form_fields)

                section_data = {
                    "appraisal_sections": {
                        "name": appraisal_section.name,
                        "description": appraisal_section.description,
                        "updated_date": appraisal_section.updated_date,
                        "created_by": appraisal_section.created_by,
                        "appraisal_year": appraisal_section.appraisal_year,
                        "appraisal_cycle_id": appraisal_section.appraisal_cycle_id,
                        "id": appraisal_section.id,
                        "created_date": appraisal_section.created_date
                    },
                    "appraisal_form": {
                        "id": appraisal_form.id,
                        "form_fields": form_fields 
                    },
                    "appraisal_submission": {
                        "submitted_by": submission.submitted_by,
                        "started_at": submission.started_at,
                        "completed_at": submission.completed_at,
                        "approval_date": submission.approval_date,
                        "completed": submission.completed,
                        "comment": submission.comment,
                        "created_date": submission.created_date,
                        "appraisal_forms_id": submission.appraisal_forms_id,
                        "submitted_values": submission.submitted_values,
                        "submitted": submission.submitted,
                        "approval_status": submission.approval_status,
                        "id": submission.id,
                        "updated_date": submission.updated_date
                    }
                }

                data.append(section_data)


        get_supervisor = db.query(StaffSupervisor).filter(StaffSupervisor.staff_id == id).first()

        if get_supervisor is None:
            supervisor_data = {
                    'id': None,
                    'full_name': None,
                }
        else:
            get_staff = db.query(Staff).filter(Staff.id == get_supervisor.supervisor_id).first()
            if get_staff is None:
                supervisor_data = {
                    'id': None,
                    'full_name': None,
                } 
            else:
                supervisor_data = {
                    'id': get_staff.id,
                    'full_name': f"{get_staff.first_name} {get_staff.last_name}" + (f" {get_staff.other_name}" if get_staff.other_name else ""),
                }


                

        get_staff_empty_info = {
            'id': get_staff_info.id,
            'title': get_staff_info.title,
            'first_name': get_staff_info.first_name,
            'last_name': get_staff_info.last_name,
            'other_name': get_staff_info.other_name,
            'full_name': f"{get_staff_info.first_name} {get_staff_info.last_name}" + (f" {get_staff_info.other_name}" if get_staff_info.other_name else ""),
            'department_id': {
                'id': get_staff_info.department.id,
                'name': get_staff_info.department.name,
            },
            'gender': get_staff_info.gender,
            'email': get_staff_info.email,
            'position': get_staff_info.position,
            'grade': get_staff_info.grade,
            'appointment_date': get_staff_info.appointment_date, 
            'role_id': {
                'id': get_staff_info.role.id,
                'name': get_staff_info.role.name,
            },
            'supervisor_id': supervisor_data,  # Update this to use the new variable
            'created_at': get_staff_info.created_date,
        }

        # Return the final response
        return {
            "staff_info": get_staff_empty_info,
            "data": data  # This contains all appraisal section and form data
        }






















    def list_appraisal(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalSchema]:
        appraisal = appraisal_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal

    def create_appraisal(self, *, db: Session, appraisal: AppraisalCreate) -> AppraisalSchema:

        check_appraisal_cycle_id = db.query(AppraisalCycle).filter(AppraisalCycle.id == appraisal.appraisal_cycles_id).first()
        if not check_appraisal_cycle_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Appraisal cycle not found")
        
        check_staff_id = db.query(Staff).filter(Staff.id == appraisal.staff_id).first()
        if not check_staff_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Staff not found")
        
        check_supervisor_id = db.query(Staff).filter(Staff.id == appraisal.supervisor_id).first()
        if not check_supervisor_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Supervisor not found")

        appraisal = appraisal_repo.create(db=db, obj_in=appraisal)
        return appraisal

    def update_appraisal(self, *, db: Session, id: UUID, appraisal: AppraisalUpdate) -> AppraisalSchema:
        appraisal_ = appraisal_repo.get(db=db, id=id)
        if not appraisal_:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal not found")
        appraisal = appraisal_repo.update(db=db, db_obj=appraisal_, obj_in=appraisal)
        return appraisal

    def get_appraisal(self, *, db: Session, id: UUID) -> AppraisalSchema:
        appraisal = appraisal_repo.get(db=db, id=id)
        if not appraisal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal not found")
        return appraisal

    def delete_appraisal(self, *, db: Session, id: UUID) -> AppraisalSchema:
        appraisal = appraisal_repo.get(db=db, id=id)
        if not appraisal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal not found")
        appraisal = appraisal_repo.remove(db=db, id=id)
        return appraisal



    def get_appraisal_by_keywords(self, *, db: Session, tag: str) -> List[AppraisalSchema]:
        pass

    def search_appraisal(self, *, db: Session, search: str, value: str) -> List[AppraisalSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return appraisal_repo.get_by_kwargs(self, db, kwargs)


appraisal_service = AppraisalService()