import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CompetencyBankListComponent } from './competency-bank-list/competency-bank-list.component';

@NgModule({
  imports: [CommonModule],
  declarations: [CompetencyBankListComponent],
  exports: [CompetencyBankListComponent],
})
export class CompetencyBankModule {}
