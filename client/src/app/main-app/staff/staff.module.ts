import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrimeNgImportsModule } from '../../shared/PrimeNgImports/PrimeNgImports.module';
import { AppTableModule } from '../../shared/app-table/app-table.module';
import { StaffListComponent } from './staff-list/staff-list.component';
import { StaffFormComponent } from './staff-form/staff-form.component';

@NgModule({
  imports: [CommonModule, PrimeNgImportsModule, AppTableModule],
  declarations: [StaffListComponent, StaffFormComponent],
  exports: [StaffListComponent],
})
export class StaffModule {}
