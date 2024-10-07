import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppraisalManagementRoutesModule } from './appraisal-management-routes.module';
import { KeyAreaModule } from './key-area/key-area.module';
import { CompetencyBankModule } from './competency-bank/competency.module';
import { MyAppraisalModule } from './my-appraisal/my-appraisal.module';
import { StaffAppraisalModule } from './staff-appraisal/staff-appraisal.module';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    AppraisalManagementRoutesModule,
    KeyAreaModule,
    CompetencyBankModule,
    MyAppraisalModule,
    StaffAppraisalModule,
  ],
})
export class AppraisalManagementModule {}
