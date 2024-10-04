import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppraisalManagementRoutesModule } from './appraisal-management-routes.module';
import { KeyAreaModule } from './key-area/key-area.module';

@NgModule({
  declarations: [],
  imports: [CommonModule, AppraisalManagementRoutesModule, KeyAreaModule],
})
export class AppraisalManagementModule {}
