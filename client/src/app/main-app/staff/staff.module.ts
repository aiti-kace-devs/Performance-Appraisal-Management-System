import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrimeNgImportsModule } from '../../shared/PrimeNgImports/PrimeNgImports.module';
import { AppTableModule } from '../../shared/app-table/app-table.module';
import { StaffListComponent } from './staff-list/staff-list.component';
import { StaffFormComponent } from './staff-form/staff-form.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { StaffSearchComponent } from './staff-search/staff-search.component';
import { errorTailorImports } from '@ngneat/error-tailor';

@NgModule({
  imports: [
    CommonModule,
    PrimeNgImportsModule,
    AppTableModule,
    FormsModule,
    ReactiveFormsModule,
    errorTailorImports,
  ],
  declarations: [StaffListComponent, StaffFormComponent, StaffSearchComponent],
  exports: [StaffListComponent, StaffSearchComponent],
})
export class StaffModule {}
