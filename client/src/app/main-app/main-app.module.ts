import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MainAppRoutesModule } from './app-routes.module';
import { StaffModule } from './staff/staff.module';

@NgModule({
  imports: [CommonModule, MainAppRoutesModule, StaffModule],
  declarations: [],
})
export class MainAppModule {}
