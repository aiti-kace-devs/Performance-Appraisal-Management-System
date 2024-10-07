import { Injectable } from '@angular/core';
import { environment } from '../../../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { IKraBank } from '../../../../shared/interfaces';

@Injectable({
  providedIn: 'root',
})
export class KeyAreaService {
  private kraURL = `${environment.API_URL_BASE}/kra_bank`;

  constructor(private http: HttpClient) {}

  getKras(id: string) {
    return this.http.get<IKraBank>(`${this.kraURL}/${id}`);
  }

  getAllKras() {
    return this.http.get<IKraBank[]>(`${this.kraURL}`);
  }

  addKra(data: any) {
    return this.http.post<IKraBank>(`${this.kraURL}`, data);
  }

  updateKra(data: any, id: string) {
    return this.http.put<IKraBank>(`${this.kraURL}/${id}`, data);
  }

  deleteKra(id: string) {
    return this.http.delete(`${this.kraURL}/${id}`);
  }
}
