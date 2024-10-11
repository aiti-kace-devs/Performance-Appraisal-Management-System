import { Injectable } from '@angular/core';
import { environment } from '../../../../../environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class StaffAppraisalService {
  private appraisalURL = `${environment.API_URL_BASE}/appraisals`;

  constructor(private http: HttpClient) {}

  getStaffAppraisal(id: string) {
    return this.http.get(`${this.appraisalURL}/${id}`);
  }
}
