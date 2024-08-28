import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { IDepartment } from '../../../shared/interfaces';

@Injectable({
  providedIn: 'root',
})
export class DepartmentService {
  private departmentURL = `${environment.API_URL_BASE}/department`;

  constructor(private http: HttpClient) {}

  getDepartment(id: string) {
    return this.http.get<IDepartment>(`${this.departmentURL}/${id}`);
  }

  getAllDepartment() {
    return this.http.get<IDepartment[]>(`${this.departmentURL}`);
  }

  addDepartment(data: any) {
    return this.http.post<IDepartment>(`${this.departmentURL}`, data);
  }

  updateDepartment(data: any, id: string) {
    return this.http.put<IDepartment>(`${this.departmentURL}/${id}`, data);
  }

  deleteDepartment(id: string) {
    return this.http.delete(`${this.departmentURL}/${id}`);
  }
}
