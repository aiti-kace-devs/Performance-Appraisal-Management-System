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
