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
import { TabViewModule } from 'primeng/tabview';
import { DropdownModule } from 'primeng/dropdown';
import { PickListModule } from 'primeng/picklist';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { TooltipModule } from 'primeng/tooltip';
import { BadgeModule } from 'primeng/badge';
import { OrderListModule } from 'primeng/orderlist';

const sharedImports = [
  ButtonModule,
  InputTextModule,
  RippleModule,
  CheckboxModule,
  StyleClassModule,
  ChipModule,
  CalendarModule,
  InputNumberModule,
  TabViewModule,
  DropdownModule,
  PickListModule,
  AutoCompleteModule,
  TooltipModule,
  BadgeModule,
  OrderListModule,
];

@NgModule({
  imports: [CommonModule, ...sharedImports],
  exports: [...sharedImports],
})
export class PrimeNgImportsModule {}
