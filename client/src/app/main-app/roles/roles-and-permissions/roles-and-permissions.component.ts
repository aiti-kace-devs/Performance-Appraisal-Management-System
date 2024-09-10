import { Component, OnInit } from '@angular/core';
import { IRole } from './../../../shared/interfaces';
import { RolesService } from '../service/roles.service';

@Component({
  selector: 'app-roles-and-permissions',
  templateUrl: './roles-and-permissions.component.html',
  styleUrl: './roles-and-permissions.component.scss',
})
export class RolesAndPermissionsComponent implements OnInit {
  roles = [];
  selectedRole: any;
  permissions = [];
  unassignedPermission: any[] = [];
  assignedPermission: any[] = [];

  constructor(private roleService: RolesService) {}

  ngOnInit() {
    this.roleService.getAllRoles().subscribe((d: any) => {
      this.roles = d;
    });

    this.roleService.getAllPermissions().subscribe((d: any) => {
      this.permissions = d;
    });
  }

  filterAssigned() {
    const ua = this.permissions.filter(
      (p: any) =>
        this.assignedPermission.findIndex((ap) => ap.id === p.id) === -1
    );

    this.unassignedPermission = ua;
  }

  onRoleChange(event: any) {
    this.roleService.getRolePermissions(event.value.id).subscribe((rp: any) => {
      this.assignedPermission = rp.permissions;
      this.filterAssigned();
    });
  }

  savePermissions() {
    console.log('data saved');
  }
}
