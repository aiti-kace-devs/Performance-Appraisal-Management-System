import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppraisalListComponent } from './appraisal-list/appraisal-list.component';
import { CycleFormComponent } from './cycle-form/cycle-form.component';
import { CycleDetailsComponent } from './cycle-details/cycle-details.component';
import { SectionFormComponent } from './section-form/section-form.component';
import { AppTableModule } from '../../../shared/app-table/app-table.module';
import { PrimeNgImportsModule } from '../../../shared/PrimeNgImports/PrimeNgImports.module';
import { RouterModule } from '@angular/router';

@NgModule({
  imports: [
    CommonModule,
    AppTableModule,
    PrimeNgImportsModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
  ],
  declarations: [
    AppraisalListComponent,
    CycleFormComponent,
    CycleDetailsComponent,
    SectionFormComponent,
  ],
  // exports: [AppraisalListComponent],
})
export class ConfigurationModule {}
