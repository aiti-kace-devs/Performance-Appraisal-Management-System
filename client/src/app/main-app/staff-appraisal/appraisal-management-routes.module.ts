import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { KeyAreaListComponent } from './key-area/key-area-list/key-area-list.component';
import { AppraisalLayoutComponent } from './appraisal/appraisal-layout/appraisal-layout.component';

const routes: Routes = [
  { path: '', component: AppraisalLayoutComponent },
  { path: 'kras-bank', component: KeyAreaListComponent },
  { path: 'competency-bank', component: KeyAreaListComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AppraisalManagementRoutesModule {}
