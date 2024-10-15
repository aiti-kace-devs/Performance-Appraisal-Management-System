export interface IStaff {
  title: string;
  first_name: string;
  last_name: string;
  other_name: string;
  full_name?: string;
  gender: string;
  email: string;
  position: string;
  department_id: IDepartment;
  grade: string;
  appointment_date: string | number | Date;
  role_id?: string;
  supervisor_id?: string;
  id?: string;
}

export interface IDepartment {
  name: string;
  description: string;
  id?: string;
  total_staff: number;
}

export interface IColumnDef {
  header: string;
  field: string;
  label?: string;
  value?: string;
  sortable?: boolean;
  subField?: string;
}

export interface IRole {
  name: string;
  id?: string;
}

export interface IUser {
  email: string;
  password?: string;
  reset_password_token: string;
  is_active: boolean;
  failed_login_attempts: number;
  account_locked_until: string | Date;
  lock_count: number;
  staff: {
    id: string;
    first_name: string;
    last_name: string;
    other_name: string;
    full_name: string;
  };
  role: IRole;
  id?: string;
}

export interface IAuthResponse {
  access_token: string;
  token_type: string;
  access_token_expiration: string | Date;
  user: {
    id: string;
    email: string;
    role_id: string;
    role: string;
  };
  refresh_token: string;
  refresh_token_expiration: string | Date;
}

export interface IStaffAppraisal {
  staff_info: IStaff;
  appraisal_cycle: IAppraisalCycle;
  data: [
    {
      appraisal_section: IAppraisalSection;
      appraisal_form: IAppraisalForm;
      submission: IAppraisalSubmission;
    }
  ];
}

export interface IAppraisalCycle {
  id?: string;
  name: string;
  description: string;
  year: string | number | Date;
  created_by?: string;
  created_date?: string | number | Date;
  updated_date?: string | number | Date;
}

export interface IAppraisalSection {
  id?: string;
  name: string;
  description: string;
  appraisal_year: number | Date;
  created_by: string;
  appraisal_cycle_id: string;
  created_date?: string | number | Date;
  updated_date?: string | number | Date;
}

export interface IAppraisalForm {
  id: string;
  form_fields: {}[];
}

export interface IAppraisalSubmission {
  id: string;
  appraisal_forms_id: string;
  submitted_by: string;
  submitted_values: {};
  started_at: string | number | Date;
  completed_at: string | number | Date;
  submitted: boolean;
  completed: boolean;
  approval_status: boolean;
  approval_date: string | number | Date;
  comment: string;
  created_date: string | number | Date;
  updated_date: string | number | Date;
}

export interface IKraBank {
  id?: string;
  department_id: string;
  created_by: string;
  focus_areas: {};
}

export interface ICompetencyBank {
  id?: string;
  competency_type: {};
}
