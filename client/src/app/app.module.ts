import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
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
import { AuthState } from './store/auth/auth.state';
import {
  HTTP_INTERCEPTORS,
  provideHttpClient,
  withInterceptorsFromDi,
} from '@angular/common/http';
import {
  errorTailorImports,
  provideErrorTailorConfig,
} from '@ngneat/error-tailor';
import {
  ERROR_MESSAGES_MAPPING,
  anchorErrorComponentFn,
  blurPrdicateFunction,
} from './config/app-config';
import { PageNotFoundComponent } from './shared/pageNotFound/pageNotFound.component';
import { TokenInterceptor } from './shared/interceptors/token-interceptor';
import { ErrorMessageInterceptor } from './shared/interceptors/error-message-interceptor';

@NgModule({
  declarations: [
    AppComponent,
    MainLayoutComponent,
    SideBarComponent,
    PageNotFoundComponent,
  ],
  bootstrap: [AppComponent],
  imports: [
    CommonModule,
    RouterOutlet,
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    AlertsModule,
    PrimeNgImportsModule,
    MainAppModule,
    NgxsModule.forRoot([StaffState, DepartmentState, AuthState]),
    errorTailorImports,
    FormsModule,
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorMessageInterceptor,
      multi: true,
    },
    provideErrorTailorConfig({
      ...ERROR_MESSAGES_MAPPING,
      blurPredicate: blurPrdicateFunction,
      controlErrorComponentAnchorFn: anchorErrorComponentFn,
    }),
    provideHttpClient(withInterceptorsFromDi()),
  ],
})
export class AppModule {}
