import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StaffComponent } from './staff.component';
import { PrimeNgImportsModule } from '../../shared/PrimeNgImports/PrimeNgImports.module';

@NgModule({
  imports: [CommonModule, PrimeNgImportsModule],
  declarations: [StaffComponent],
  exports: [StaffComponent],
})
export class StaffModule {}
