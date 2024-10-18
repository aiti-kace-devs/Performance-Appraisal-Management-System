import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppraisalManagementRoutesModule } from './appraisal-management-routes.module';
import { KeyAreaBankModule } from './key-area/key-area-bank.module';
import { CompetencyBankModule } from './competency-bank/competency.module';
import { MyAppraisalModule } from './my-appraisal/my-appraisal.module';
import { StaffAppraisalModule } from './staff-appraisal/staff-appraisal.module';
import { ConfigurationModule } from './configuration/configuration.module';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    AppraisalManagementRoutesModule,
    KeyAreaBankModule,
    CompetencyBankModule,
    MyAppraisalModule,
    StaffAppraisalModule,
    ConfigurationModule,
  ],
})
export class AppraisalManagementModule {}
