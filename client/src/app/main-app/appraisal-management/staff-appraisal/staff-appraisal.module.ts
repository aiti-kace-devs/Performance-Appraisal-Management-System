import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StaffAppraisalListComponent } from './staff-appraisal-list/staff-appraisal-list.component';
import { AppraisalLayoutComponent } from './appraisal-layout/appraisal-layout.component';
import { StaffAppraisalSectionComponent } from './staff-appraisal-section/staff-appraisal-section.component';
import { AppTableModule } from '../../../shared/app-table/app-table.module';
import { PrimeNgImportsModule } from '../../../shared/PrimeNgImports/PrimeNgImports.module';
import { RouterModule } from '@angular/router';

@NgModule({
  imports: [CommonModule, AppTableModule, PrimeNgImportsModule, RouterModule],
  declarations: [
    StaffAppraisalListComponent,
    AppraisalLayoutComponent,
    StaffAppraisalSectionComponent,
  ],
  exports: [StaffAppraisalListComponent],
})
export class StaffAppraisalModule {}
