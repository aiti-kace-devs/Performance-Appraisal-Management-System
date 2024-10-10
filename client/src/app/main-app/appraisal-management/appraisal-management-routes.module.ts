import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { KeyAreaListComponent } from './key-area/key-area-list/key-area-list.component';
import { AppraisalLayoutComponent } from './staff-appraisal/appraisal-layout/appraisal-layout.component';
import { CompetencyBankListComponent } from './competency-bank/competency-bank-list/competency-bank-list.component';
import { MyAppraisalListComponent } from './my-appraisal/my-appraisal-list/my-appraisal-list.component';
import { StaffAppraisalListComponent } from './staff-appraisal/staff-appraisal-list/staff-appraisal-list.component';

const routes: Routes = [
  { path: '', component: StaffAppraisalListComponent },
  { path: 'my-appraisal', component: MyAppraisalListComponent },
  { path: 'configuration', component: AppraisalLayoutComponent },
  { path: 'kras-bank', component: KeyAreaListComponent },
  { path: 'competency-bank', component: CompetencyBankListComponent },
  { path: 'details/:id', component: AppraisalLayoutComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AppraisalManagementRoutesModule {}