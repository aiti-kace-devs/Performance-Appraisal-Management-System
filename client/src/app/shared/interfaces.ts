export interface IStaff {
  title: string;
  first_name: string;
  last_name: string;
  other_name: string;
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
}

export interface IColumnDef {
  header: string;
  field: string;
  label?: string;
  value?: string;
}
