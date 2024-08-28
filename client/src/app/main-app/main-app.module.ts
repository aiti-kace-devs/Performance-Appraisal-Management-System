import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainAppRoutesModule } from './app-routes.module';
import { StaffModule } from './staff/staff.module';
import { DepartmentModule } from './department/department.module';

@NgModule({
  imports: [CommonModule, MainAppRoutesModule, StaffModule, DepartmentModule],
  declarations: [],
})
export class MainAppModule {}
