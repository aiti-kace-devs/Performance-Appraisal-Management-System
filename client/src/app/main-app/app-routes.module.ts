import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { StaffListComponent } from './staff/staff-list/staff-list.component';
import { DepartmentListComponent } from './department/department-list/department-list.component';
import { ReportsComponent } from './reports/reports.component';
import { RolesLayoutComponent } from './roles/roles-layout/roles-layout.component';

const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'staff', component: StaffListComponent },
  { path: 'department', component: DepartmentListComponent },
  { path: 'reports', component: ReportsComponent },
  { path: 'roles', component: RolesLayoutComponent },
  {
    path: 'appraisal-management',
    loadChildren: () =>
      import('./appraisal-management/appraisal-management.module').then(
        (m) => m.AppraisalManagementModule
      ),
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class MainAppRoutesModule {}
