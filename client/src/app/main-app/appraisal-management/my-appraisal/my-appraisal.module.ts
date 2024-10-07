import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MyAppraisalListComponent } from './my-appraisal-list/my-appraisal-list.component';

@NgModule({
  declarations: [MyAppraisalListComponent],
  exports: [MyAppraisalListComponent],
  imports: [CommonModule],
})
export class MyAppraisalModule {}
