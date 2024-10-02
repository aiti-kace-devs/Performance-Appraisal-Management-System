import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DepartmentListComponent } from './department-list/department-list.component';
import { DepartmentFormComponent } from './department-form/department-form.component';
import { DepartmentMembersComponent } from './department-members/department-members.component';
import { PrimeNgImportsModule } from '../../shared/PrimeNgImports/PrimeNgImports.module';
import { AppTableModule } from '../../shared/app-table/app-table.module';
import { errorTailorImports } from '@ngneat/error-tailor';

@NgModule({
  declarations: [
    DepartmentListComponent,
    DepartmentFormComponent,
    DepartmentMembersComponent,
  ],
  imports: [
    CommonModule,
    PrimeNgImportsModule,
    AppTableModule,
    FormsModule,
    ReactiveFormsModule,
    errorTailorImports,
  ],
  exports: [DepartmentListComponent],
})
export class DepartmentModule {}
