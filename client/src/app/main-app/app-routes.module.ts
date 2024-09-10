import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { StaffListComponent } from './staff/staff-list/staff-list.component';
import { DepartmentListComponent } from './department/department-list/department-list.component';
import { StaffAppraisalComponent } from './staff-appraisal/staff-appraisal.component';
import { ReportsComponent } from './reports/reports.component';
import { RolesLayoutComponent } from './roles/roles-layout/roles-layout.component';

const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'staff', component: StaffListComponent },
  { path: 'department', component: DepartmentListComponent },
  { path: 'appraisal', component: StaffAppraisalComponent },
  { path: 'reports', component: ReportsComponent },
  { path: 'roles', component: RolesLayoutComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class MainAppRoutesModule {}
