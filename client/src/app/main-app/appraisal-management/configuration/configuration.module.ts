import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppraisalListComponent } from './appraisal-list/appraisal-list.component';
import { CycleFormComponent } from './cycle-form/cycle-form.component';
import { CycleDetailsComponent } from './cycle-details/cycle-details.component';
import { CycleSectionComponent } from './cycle-section/cycle-section.component';
import { SectionFormComponent } from './section-form/section-form.component';
import { ConfigurationLayoutComponent } from './configuration-layout/configuration-layout.component';
import { CycleFormDialogComponent } from './cycle-form/cycle-form-dialog.component';
import { AppTableModule } from '../../../shared/app-table/app-table.module';
import { PrimeNgImportsModule } from '../../../shared/PrimeNgImports/PrimeNgImports.module';
import { RouterModule } from '@angular/router';
import { errorTailorImports } from '@ngneat/error-tailor';

@NgModule({
  imports: [
    CommonModule,
    AppTableModule,
    PrimeNgImportsModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    errorTailorImports,
  ],
  declarations: [
    AppraisalListComponent,
    CycleFormComponent,
    CycleDetailsComponent,
    SectionFormComponent,
    ConfigurationLayoutComponent,
    CycleSectionComponent,
    CycleFormDialogComponent,
  ],
  exports: [CycleFormComponent],
})
export class ConfigurationModule {}
