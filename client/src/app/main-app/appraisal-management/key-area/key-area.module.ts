import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { KeyAreaListComponent } from './key-area-list/key-area-list.component';
import { AppTableModule } from '../../../shared/app-table/app-table.module';
import { PrimeNgImportsModule } from '../../../shared/PrimeNgImports/PrimeNgImports.module';

@NgModule({
  imports: [CommonModule, AppTableModule, PrimeNgImportsModule],
  declarations: [KeyAreaListComponent],
  exports: [KeyAreaListComponent],
})
export class KeyAreaModule {}
