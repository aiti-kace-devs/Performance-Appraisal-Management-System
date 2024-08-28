import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { RippleModule } from 'primeng/ripple';
import { CheckboxModule } from 'primeng/checkbox';
import { StyleClassModule } from 'primeng/styleclass';
import { ChipModule } from 'primeng/chip';
import { CalendarModule } from 'primeng/calendar';
import { InputNumberModule } from 'primeng/inputnumber';

const sharedImports = [
  ButtonModule,
  InputTextModule,
  RippleModule,
  CheckboxModule,
  StyleClassModule,
  ChipModule,
  CalendarModule,
  InputNumberModule,
];

@NgModule({
  imports: [CommonModule, ...sharedImports],
  exports: [...sharedImports],
})
export class PrimeNgImportsModule {}
