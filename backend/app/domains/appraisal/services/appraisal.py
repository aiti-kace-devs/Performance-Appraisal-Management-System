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
from datetime import datetime



class AppraisalService:





    def get_appraisal_by_id(self, db: Session, staff_id: UUID):
        get_staff_empty_info = {}
        data = []
        supervisor_data = {}

        date = datetime.now()
        current_year = date.year

        get_supervisor = db.query(StaffSupervisor).filter(StaffSupervisor.staff_id == staff_id, StaffSupervisor.appraisal_year == current_year).first()
        if get_supervisor:
            get_staff = db.query(Staff).filter(Staff.id == get_supervisor.supervisor_id).first()
            if get_staff:
                supervisor_data = {
                    'id': get_staff.id,
                    'full_name': f"{get_staff.first_name} {get_staff.last_name}" + (f" {get_staff.other_name}" if get_staff.other_name else ""),
                }
            else:
                supervisor_data = {
                    'id': None,
                    'full_name': None,
                }
        else:
            supervisor_data = {
                'id': None,
                'full_name': None,
            }

        get_staff_info = db.query(Staff).filter(Staff.id == staff_id).first()

        if not get_staff_info:
            return {
                "staff_info": {},
                "appraisal_cycle": {},
                "data": []
            }

        appraisal_sections = db.query(AppraisalSection).filter(
            AppraisalSection.created_by == supervisor_data.get('id'),
            AppraisalSection.appraisal_year == current_year
        ).all()

        for section in appraisal_sections:
            appraisal_form = db.query(AppraisalForm).filter(AppraisalForm.appraisal_sections_id == section.id).first()

            form_fields = json.loads(appraisal_form.form_fields) if appraisal_form else {}
            get_staff_appraisal_submission = []

            if appraisal_form:
                get_staff_appraisal_submission = db.query(AppraisalSubmission).filter(
                    AppraisalSubmission.appraisal_forms_id == appraisal_form.id
                ).all()

            if get_staff_appraisal_submission:
                for submission in get_staff_appraisal_submission:
                    section_data = {
                        "appraisal_section": {
                            "id": section.id,
                            "name": section.name,
                            "description": section.description,
                            "appraisal_year": section.appraisal_year,
                            "created_by": section.created_by,
                            "appraisal_cycle_id": section.appraisal_cycle_id,
                            "created_date": section.created_date,
                            "updated_date": section.updated_date,
                        },
                        "appraisal_form": {
                            "id": appraisal_form.id if appraisal_form else None,
                            "form_fields": form_fields
                        },
                        "submission": {
                            "id": submission.id,
                            "submitted_by": submission.submitted_by,
                            "started_at": submission.started_at,
                            "completed_at": submission.completed_at,
                            "approval_date": submission.approval_date,
                            "completed": submission.completed,
                            "comment": submission.comment,
                            "appraisal_forms_id": submission.appraisal_forms_id,
                            "submitted_values": submission.submitted_values,
                            "submitted": submission.submitted,
                            "approval_status": submission.approval_status,
                            "created_date": submission.created_date,
                            "updated_date": submission.updated_date
                        }
                    }
                    data.append(section_data)
            else:
                section_data = {
                    "appraisal_section": {
                        "id": section.id,
                        "name": section.name,
                        "description": section.description,
                        "appraisal_year": section.appraisal_year,
                        "created_by": section.created_by,
                        "appraisal_cycle_id": section.appraisal_cycle_id,
                        "created_date": section.created_date,
                        "updated_date": section.updated_date,
                    },
                    "appraisal_form": {
                        "id": appraisal_form.id if appraisal_form else None,
                        "form_fields": form_fields
                    },
                    "submission": None
                }
                data.append(section_data)

        get_appraisal_cycle = db.query(AppraisalCycle).filter(
            AppraisalCycle.created_by == supervisor_data.get('id'),
            AppraisalCycle.year == current_year
        ).first()

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
            'supervisor_id': supervisor_data,
            'created_at': get_staff_info.created_date,
        }

        return {
            "staff_info": get_staff_empty_info,
            "appraisal_cycle": get_appraisal_cycle or None,
            "data": data
        }
    













































    def get_staff_appraisals_by_staff_id_and_appraisal_year(self, db: Session, staff_id: UUID, appraisal_year: int,):
        get_staff_empty_info = {}
        data = []
        supervisor_data = {}

        date = datetime.now()
        current_year = date.year

        get_supervisor = db.query(StaffSupervisor).filter(StaffSupervisor.staff_id == staff_id).first()
        if get_supervisor:
            get_staff = db.query(Staff).filter(Staff.id == get_supervisor.supervisor_id, StaffSupervisor.appraisal_year == appraisal_year).first()
            if get_staff:
                supervisor_data = {
                    'id': get_staff.id,
                    'full_name': f"{get_staff.first_name} {get_staff.last_name}" + (f" {get_staff.other_name}" if get_staff.other_name else ""),
                }
            else:
                supervisor_data = {
                    'id': None,
                    'full_name': None,
                }
        else:
            supervisor_data = {
                'id': None,
                'full_name': None,
            }

        get_staff_info = db.query(Staff).filter(Staff.id == staff_id).first()

        if not get_staff_info:
            return {
                "staff_info": {},
                "appraisal_cycle": {},
                "data": []
            }

        appraisal_sections = db.query(AppraisalSection).filter(
            AppraisalSection.created_by == supervisor_data.get('id'),
            AppraisalSection.appraisal_year == appraisal_year
        ).all()

        for section in appraisal_sections:
            appraisal_form = db.query(AppraisalForm).filter(AppraisalForm.appraisal_sections_id == section.id).first()

            form_fields = json.loads(appraisal_form.form_fields) if appraisal_form else {}
            get_staff_appraisal_submission = []

            if appraisal_form:
                get_staff_appraisal_submission = db.query(AppraisalSubmission).filter(
                    AppraisalSubmission.appraisal_forms_id == appraisal_form.id
                ).all()

            if get_staff_appraisal_submission:
                for submission in get_staff_appraisal_submission:
                    section_data = {
                        "appraisal_section": {
                            "id": section.id,
                            "name": section.name,
                            "description": section.description,
                            "appraisal_year": section.appraisal_year,
                            "created_by": section.created_by,
                            "appraisal_cycle_id": section.appraisal_cycle_id,
                            "created_date": section.created_date,
                            "updated_date": section.updated_date,
                        },
                        "appraisal_form": {
                            "id": appraisal_form.id if appraisal_form else None,
                            "form_fields": form_fields
                        },
                        "submission": {
                            "id": submission.id,
                            "submitted_by": submission.submitted_by,
                            "started_at": submission.started_at,
                            "completed_at": submission.completed_at,
                            "approval_date": submission.approval_date,
                            "completed": submission.completed,
                            "comment": submission.comment,
                            "appraisal_forms_id": submission.appraisal_forms_id,
                            "submitted_values": submission.submitted_values,
                            "submitted": submission.submitted,
                            "approval_status": submission.approval_status,
                            "created_date": submission.created_date,
                            "updated_date": submission.updated_date
                        }
                    }
                    data.append(section_data)
            else:
                section_data = {
                    "appraisal_section": {
                        "id": section.id,
                        "name": section.name,
                        "description": section.description,
                        "appraisal_year": section.appraisal_year,
                        "created_by": section.created_by,
                        "appraisal_cycle_id": section.appraisal_cycle_id,
                        "created_date": section.created_date,
                        "updated_date": section.updated_date,
                    },
                    "appraisal_form": {
                        "id": appraisal_form.id if appraisal_form else None,
                        "form_fields": form_fields
                    },
                    "submission": None
                }
                data.append(section_data)

        get_appraisal_cycle = db.query(AppraisalCycle).filter(
            AppraisalCycle.created_by == supervisor_data.get('id'),
            AppraisalCycle.year == appraisal_year
        ).first()

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
            'supervisor_id': supervisor_data,
            'created_at': get_staff_info.created_date,
        }

        return {
            "staff_info": get_staff_empty_info,
            "appraisal_cycle": get_appraisal_cycle or None,
            "data": data
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