import { Injectable } from '@angular/core';
import { environment } from '../../../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { IAppraisalCycle } from '../../../../shared/interfaces';

@Injectable({
  providedIn: 'root',
})
export class ConfigurationService {
  private appraisalCycleURL = `${environment.API_URL_BASE}/appraisal_cycles`;
  private appraisalSectionURL = `${environment.API_URL_BASE}/appraisal_sections`;

  constructor(private http: HttpClient) {}

  getAllCycle() {
    return this.http.get<IAppraisalCycle[]>(`${this.appraisalCycleURL}/all`);
  }

  addCycle(data: IAppraisalCycle) {
    return this.http.post<IAppraisalCycle>(
      `${this.appraisalCycleURL}/new`,
      data
    );
  }

  updateCycle(data: any, id: string) {
    return this.http.put<IAppraisalCycle>(
      `${this.appraisalCycleURL}/${id}`,
      data
    );
  }

  deleteCycle(id: string) {
    return this.http.delete(`${this.appraisalCycleURL}/${id}`);
  }

  getCycleWithSections(id: string) {
    return this.http.get<IAppraisalCycle>(`${this.appraisalCycleURL}/${id}`);
  }

  updateCycleSections(data: any, id: string) {
    return this.http.put<IAppraisalCycle>(
      `${this.appraisalSectionURL}/${id}`,
      data
    );
  }
}
