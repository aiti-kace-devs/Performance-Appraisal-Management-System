from datetime import date,time,datetime
from typing import Optional, Any, Dict,List
import uuid
from pydantic import BaseModel, Field, field_validator
from pydantic import UUID4


class GetDepartmentBase(BaseModel):
     id: UUID4
     name: str



class GetRoleBase(BaseModel):
     id: UUID4
     name: str



class GetSupervisorBase(BaseModel):
     id: UUID4
     full_name: str



class GetStaffBase(BaseModel):
    id: UUID4
    title: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    other_name: Optional[str]
    full_name: Optional[str]
    gender: Optional[str]
    email: Optional[str]
    position: Optional[str]
    grade: Optional[str]
    appointment_date: Optional[date]
    department: Optional[GetDepartmentBase] = None
    role: Optional[GetRoleBase] = None
    supervisor: Optional[GetSupervisorBase] = None
    created_date: Optional[datetime]





class GetAppraisalCycleBase(BaseModel):
    id: UUID4
    name: Optional[str]
    description: Optional[str]
    year: Optional[int]
    created_by: Optional[UUID4]
    created_date: Optional[datetime]
    updated_date: Optional[datetime]





class GetAppraisalSectionBase(BaseModel):
    id: UUID4
    name: Optional[str]
    description: Optional[str]
    appraisal_year: Optional[int]
    created_by: Optional[UUID4]
    appraisal_cycle_id: Optional[UUID4]
    created_date: Optional[datetime]
    updated_date: Optional[datetime]




class ReadAppraisalFormBase(BaseModel):
    id: Optional[UUID4]
    form_fields : List[Dict]





class ReadAppraisalSubmissionBase(BaseModel):
    id : Optional[UUID4]
    appraisal_forms_id : Optional[UUID4]
    submitted_by : Optional[UUID4]
    submitted_values : Dict[str, Any]
    started_at : Optional[date]
    completed_at : Optional[date]
    submitted : Optional[bool]
    completed : Optional[bool]
    approval_status : Optional[bool]
    approval_date : Optional[date]
    comment : Optional[str]
    created_date : Optional[datetime]
    updated_date : Optional[datetime]





class AppraisalDataBase(BaseModel):
    appraisal_section: Optional[GetAppraisalSectionBase] = None
    appraisal_form: Optional[ReadAppraisalFormBase] = None
    submission: Optional[ReadAppraisalSubmissionBase] = None




class GetStaffAppraisalBase(BaseModel):
    staff_info: Optional[GetStaffBase] = None
    appraisal_cycle: Optional[GetAppraisalCycleBase] = None
    data: Optional[List[AppraisalDataBase]] = None
