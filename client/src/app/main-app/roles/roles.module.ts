import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PrimeNgImportsModule } from '../../shared/PrimeNgImports/PrimeNgImports.module';
import { StaffModule } from '../staff/staff.module';
import { errorTailorImports } from '@ngneat/error-tailor';
import { RolesLayoutComponent } from './roles-layout/roles-layout.component';
import { RolesAndPermissionsComponent } from './roles-and-permissions/roles-and-permissions.component';

@NgModule({
  declarations: [RolesLayoutComponent, RolesAndPermissionsComponent],
  imports: [
    CommonModule,
    PrimeNgImportsModule,
    StaffModule,
    FormsModule,
    ReactiveFormsModule,
    errorTailorImports,
  ],
  exports: [],
})
export class RolesModule {}
