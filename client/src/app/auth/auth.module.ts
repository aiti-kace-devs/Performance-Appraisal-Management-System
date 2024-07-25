import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthRoutesModule } from './auth-routes.module';
import { LoginComponent } from './login/login.component';
import { PrimeNgImportsModule } from '../shared/PrimeNgImports/PrimeNgImports.module';

@NgModule({
  imports: [CommonModule, AuthRoutesModule, PrimeNgImportsModule],
  declarations: [LoginComponent],
})
export class AuthModule {}
