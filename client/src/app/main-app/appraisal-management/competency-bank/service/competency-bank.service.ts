import { Injectable } from '@angular/core';
import { environment } from '../../../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { ICompetencyBank } from '../../../../shared/interfaces';

@Injectable({
  providedIn: 'root',
})
export class CompetencyBankService {
  private competencyURL = `${environment.API_URL_BASE}/competency_banks`;

  constructor(private http: HttpClient) {}

  getCompetency(id: string) {
    return this.http.get<ICompetencyBank>(`${this.competencyURL}/${id}`);
  }

  getAllCompetency() {
    return this.http.get<ICompetencyBank[]>(`${this.competencyURL}`);
  }

  addCompetency(data: any) {
    return this.http.post<ICompetencyBank>(`${this.competencyURL}`, data);
  }

  updateCompetency(data: any, id: string) {
    return this.http.put<ICompetencyBank>(`${this.competencyURL}/${id}`, data);
  }

  deleteCompetency(id: string) {
    return this.http.delete(`${this.competencyURL}/${id}`);
  }
}
