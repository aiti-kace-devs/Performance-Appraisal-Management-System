import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DepartmentListComponent } from './department-list/department-list.component';
import { DepartmentFormComponent } from './department-form/department-form.component';
import { PrimeNgImportsModule } from '../../shared/PrimeNgImports/PrimeNgImports.module';
import { AppTableModule } from '../../shared/app-table/app-table.module';

@NgModule({
  declarations: [DepartmentListComponent, DepartmentFormComponent],
  imports: [
    CommonModule,
    PrimeNgImportsModule,
    AppTableModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  exports: [DepartmentListComponent],
})
export class DepartmentModule {}
