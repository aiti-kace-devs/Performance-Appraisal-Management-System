import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PrimeNgImportsModule } from '../../shared/PrimeNgImports/PrimeNgImports.module';
import { AppTableModule } from '../../shared/app-table/app-table.module';
import { errorTailorImports } from '@ngneat/error-tailor';
import { RolesLayoutComponent } from './roles-layout/roles-layout.component';
import { RolesAndPermissionsComponent } from './roles-and-permissions/roles-and-permissions.component';
import { StaffPermissionsComponent } from './staff-permissions/staff-permissions.component';

@NgModule({
  declarations: [
    RolesLayoutComponent,
    RolesAndPermissionsComponent,
    StaffPermissionsComponent,
  ],
  imports: [
    CommonModule,
    PrimeNgImportsModule,
    AppTableModule,
    FormsModule,
    ReactiveFormsModule,
    errorTailorImports,
  ],
  exports: [],
})
export class RolesModule {}
