import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CompetencyBankListComponent } from './competency-bank-list/competency-bank-list.component';
import { AppTableModule } from '../../../shared/app-table/app-table.module';
import { PrimeNgImportsModule } from '../../../shared/PrimeNgImports/PrimeNgImports.module';

@NgModule({
  imports: [CommonModule, AppTableModule, PrimeNgImportsModule],
  declarations: [CompetencyBankListComponent],
  exports: [CompetencyBankListComponent],
})
export class CompetencyBankModule {}
