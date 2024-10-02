import { Component, Input, OnInit } from '@angular/core';
import { RolesService } from '../service/roles.service';
import { AppAlertService } from '../../../shared/alerts/service/app-alert.service';
import { PrimeNgAlerts } from '../../../config/app-config';

@Component({
  selector: 'app-roles-and-permissions',
  templateUrl: './roles-and-permissions.component.html',
  styleUrl: './roles-and-permissions.component.scss',
})
export class RolesAndPermissionsComponent implements OnInit {
  @Input() isRoleSelect = true;
  roles = [];
  selectedRole: any;
  permissions = [];
  unassignedPermission: any[] = [];
  assignedPermission: any[] = [];
  originalAssignedPermissions: any[] = [];

  constructor(
    private roleService: RolesService,
    private alert: AppAlertService
  ) {}

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
      const permissions = rp.permissions;
      this.assignedPermission = permissions;
      this.originalAssignedPermissions = [...permissions];
      this.filterAssigned();
    });
  }

  savePermissions() {
    if (!this.noChange) {
      const data = {
        new_permissions: this.assignedPermission.map((p) => p.id),
      };

      if (this.isRoleSelect) {
        this.roleService
          .updateRolePermissions(data, this.selectedRole.id)
          .subscribe((d) => {
            this.alert.showToast('Permissions Updated', PrimeNgAlerts.SUCCESS);
          });
      } else {
        console.log('hey you');
      }
    }
  }

  get noChange() {
    return (
      this.assignedPermission?.length === 0 ||
      (this.assignedPermission?.length > 0 &&
        this.originalAssignedPermissions.length > 0 &&
        this.assignedPermission?.length ===
          this.originalAssignedPermissions?.length &&
        this.originalAssignedPermissions?.every((perm) =>
          this.assignedPermission.includes(perm)
        ) &&
        this.assignedPermission?.every((perm) =>
          this.originalAssignedPermissions.includes(perm)
        ))
    );
  }
}
