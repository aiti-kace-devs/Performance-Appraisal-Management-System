from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.base_class import UUID
from domains.appraisal.schemas.appraisal import GetStaffAppraisalBase
from domains.appraisal.models.appraisal_cycle import AppraisalCycle
from domains.appraisal.models.staff_role_permissions import Staff
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.models.appraisal_submission import AppraisalSubmission
from domains.appraisal.models.appraisal_form import AppraisalForm
from domains.appraisal.models.staff_supervisor import StaffSupervisor
import json
from datetime import datetime



class AppraisalService:





    def get_appraisal_by_id(self, db: Session, staff_id: UUID) -> GetStaffAppraisalBase:
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
                            "form_fields": [form_fields]
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
                        "form_fields": [form_fields]
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
            'gender': get_staff_info.gender,
            'email': get_staff_info.email,
            'position': get_staff_info.position,
            'grade': get_staff_info.grade,
            'appointment_date': get_staff_info.appointment_date,
            'department': {
                'id': get_staff_info.department.id,
                'name': get_staff_info.department.name,
            },
            'role': {
                'id': get_staff_info.role.id,
                'name': get_staff_info.role.name,
            },
            'supervisor': supervisor_data,
            'created_date': get_staff_info.created_date,
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

        get_supervisor = db.query(StaffSupervisor).filter(StaffSupervisor.staff_id == staff_id, StaffSupervisor.appraisal_year == appraisal_year).first()
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
                            "form_fields": [form_fields]
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
                        "form_fields": [form_fields]
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
            'gender': get_staff_info.gender,
            'email': get_staff_info.email,
            'position': get_staff_info.position,
            'grade': get_staff_info.grade,
            'appointment_date': get_staff_info.appointment_date,
            'department': {
                'id': get_staff_info.department.id,
                'name': get_staff_info.department.name,
            },
            'role': {
                'id': get_staff_info.role.id,
                'name': get_staff_info.role.name,
            },
            'supervisor': supervisor_data,
            'created_date': get_staff_info.created_date,
        }

        return {
            "staff_info": get_staff_empty_info,
            "appraisal_cycle": get_appraisal_cycle or None,
            "data": data
        }






appraisal_service = AppraisalService()