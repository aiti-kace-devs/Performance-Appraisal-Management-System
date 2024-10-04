import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppraisalLayoutComponent } from './appraisal-layout/appraisal-layout.component';

@NgModule({
  imports: [CommonModule],
  declarations: [AppraisalLayoutComponent],
  exports: [AppraisalLayoutComponent],
})
export class AppraisalModule {}
