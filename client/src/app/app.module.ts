import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { AppComponent } from './app.component';
import { RouterOutlet } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { AlertsModule } from './shared/alerts/alerts.module';
import { PrimeNgImportsModule } from './shared/PrimeNgImports/PrimeNgImports.module';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';
import { SideBarComponent } from './layout/side-bar/side-bar.component';
import { MainAppModule } from './main-app/main-app.module';
import { NgxsModule } from '@ngxs/store';
import { StaffState } from './store/staff/staff.state';
import { DepartmentState } from './store/department/department.state';
import { HttpClientModule } from '@angular/common/http';
import {
  errorTailorImports,
  provideErrorTailorConfig,
} from '@ngneat/error-tailor';
import {
  ERROR_MESSAGES_MAPPING,
  anchorErrorComponentFn,
  blurPrdicateFunction,
} from './config/app-config';

@NgModule({
  declarations: [AppComponent, MainLayoutComponent, SideBarComponent],
  imports: [
    CommonModule,
    RouterOutlet,
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    AlertsModule,
    PrimeNgImportsModule,
    MainAppModule,
    HttpClientModule,
    NgxsModule.forRoot([StaffState, DepartmentState]),
    errorTailorImports,
  ],
  providers: [
    provideErrorTailorConfig({
      ...ERROR_MESSAGES_MAPPING,
      blurPredicate: blurPrdicateFunction,
      controlErrorComponentAnchorFn: anchorErrorComponentFn,
    }),
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
