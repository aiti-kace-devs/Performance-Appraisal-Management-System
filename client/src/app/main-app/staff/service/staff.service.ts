import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { IStaff } from '../../../shared/interfaces';
import { catchError, map, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StaffService {
  private staffURL = `${environment.API_URL_BASE}/staff`;

  constructor(private http: HttpClient) {}

  getStaff(id: string) {
    return this.http.get<IStaff>(`${this.staffURL}/${id}`);
  }

  getAllStaff() {
    return this.http.get<IStaff[]>(`${this.staffURL}`);
  }

  addStaff(data: any) {
    return this.http.post<IStaff>(`${this.staffURL}`, data);
  }

  updateStaff(data: any, id: string) {
    return this.http.put<IStaff>(`${this.staffURL}/${id}`, data);
  }

  deleteStaff(id: string) {
    return this.http.delete(`${this.staffURL}/${id}`);
  }

  userEmailExists(email: string) {
    return this.http.get(`${this.staffURL}/email/${email}`).pipe(
      catchError(() => of(true)),
      map((d: any) => d as boolean)
    );
  }
}
