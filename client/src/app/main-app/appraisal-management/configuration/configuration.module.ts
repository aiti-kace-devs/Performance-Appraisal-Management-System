import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppraisalListComponent } from './appraisal-list/appraisal-list.component';
import { CycleFormComponent } from './cycle-form/cycle-form.component';
import { AppTableModule } from '../../../shared/app-table/app-table.module';
import { PrimeNgImportsModule } from '../../../shared/PrimeNgImports/PrimeNgImports.module';

@NgModule({
  imports: [
    CommonModule,
    AppTableModule,
    PrimeNgImportsModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  declarations: [AppraisalListComponent, CycleFormComponent],
  // exports: [AppraisalListComponent],
})
export class ConfigurationModule {}
