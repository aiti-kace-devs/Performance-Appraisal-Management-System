import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthRoutesModule } from './auth-routes.module';
import { LoginComponent } from './login/login.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { PrimeNgImportsModule } from '../shared/PrimeNgImports/PrimeNgImports.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  imports: [
    CommonModule,
    AuthRoutesModule,
    PrimeNgImportsModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  declarations: [LoginComponent, ForgotPasswordComponent],
  exports: [LoginComponent],
})
export class AuthModule {}
