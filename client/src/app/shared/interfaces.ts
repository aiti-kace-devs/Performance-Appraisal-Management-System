export interface IStaff {
  title: string;
  first_name: string;
  last_name: string;
  other_name: string;
  full_name?: string;
  gender: string;
  email: string;
  position: string;
  department_id: string;
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
