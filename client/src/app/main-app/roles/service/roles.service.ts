import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { IRole } from '../../../shared/interfaces';

@Injectable({
  providedIn: 'root',
})
export class RolesService {
  private rolesURL = `${environment.API_URL_BASE}/roles`;
  private permissionURL = `${environment.API_URL_BASE}/perms`;
  private rolePermissionURL = `${environment.API_URL_BASE}/roles-permission`;

  constructor(private http: HttpClient) {}

  getRole(id: string) {
    return this.http.get<IRole>(`${this.rolesURL}/${id}`);
  }

  getAllRoles() {
    return this.http.get(`${this.rolesURL}`);
  }

  getAllPermissions() {
    return this.http.get(`${this.permissionURL}`);
  }

  getRolePermissions(id: string) {
    return this.http.get(`${this.rolePermissionURL}/${id}`);
  }

  updateRolePermissions(data: any, id: string) {
    return this.http.put(`${this.rolePermissionURL}/${id}`, data);
  }
}
