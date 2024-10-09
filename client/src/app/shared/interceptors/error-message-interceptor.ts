import { retry, tap } from 'rxjs/operators';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import {
  BehaviorSubject,
  EMPTY,
  Observable,
  catchError,
  switchMap,
  take,
  throwError,
} from 'rxjs';
import { APP_REFRESH_TOKEN, PrimeNgAlerts } from '../../config/app-config';
import { AppAlertService } from '../alerts/service/app-alert.service';
import { LoginService } from '../../auth/service/login.service';

@Injectable()
export class ErrorMessageInterceptor implements HttpInterceptor {
  tokenSubject = new BehaviorSubject<string | null>(null);
  retries = 0;

  constructor(
    private alert: AppAlertService,
    private loginService: LoginService,
    private router: Router
  ) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      catchError((event: any) => {
        if (event.status === 400) {
          this.alert.showToast(`${event.error.detail}`, PrimeNgAlerts.ERROR);
        } else if (event.status === 401 && request.url.includes('auth/token')) {
          this.alert.showToast(
            `Invalid credentials entered`,
            PrimeNgAlerts.ERROR
          );
        } else if (event.status === 401 && !request.url.includes('refresh')) {
          const refreshToken = localStorage.getItem(APP_REFRESH_TOKEN);
          const isLoggedIn =
            typeof this.loginService.loggedInUser?.id !== 'undefined';
          if (refreshToken && this.retries < 2) {
            return this.loginService.requestNewAccessToken(refreshToken).pipe(
              retry(1),
              tap(() => this.retries++),
              switchMap((result) => {
                if (result) {
                  return next.handle(request).pipe(
                    catchError((err) => {
                      if (
                        this.retries > 0 &&
                        err.status == 401 &&
                        !isLoggedIn
                      ) {
                        this.handleTokenExpiredException();
                      }
                      return EMPTY;
                    })
                  );
                } else {
                  this.handleTokenExpiredException();

                  return EMPTY;
                }
              })
            );
          } else {
            if (!isLoggedIn) {
              this.handleTokenExpiredException();
            }
          }
        } else if (
          (event.status === 401 && request.url.includes('refresh')) ||
          event.error?.message === 'Refresh Token is invalid'
        ) {
          this.handleTokenExpiredException();
        } else if (event.status === 403) {
          this.alert.showToast(
            `Sorry you are not permitted to perform this function. See administrator`,
            PrimeNgAlerts.ERROR
          );
        } else if (event.status === 422) {
          if (!request.url.includes('/auth')) {
            this.alert.showToast(
              event.error?.message || `Unable to process request`,
              PrimeNgAlerts.ERROR
            );
          } else {
            return throwError(() => event);
          }
        } else if (event.status === 404) {
          const dontShowErrorRoutes = ['register'];
          const currentPath = window.location.pathname;
          const dontShow = dontShowErrorRoutes.some((route) =>
            currentPath.includes(route)
          );

          if (!dontShow) {
            this.alert.showToast(`Not found`, PrimeNgAlerts.ERROR);
          }
        } else if (event.error?.message && event.status >= 500) {
          this.alert.showToast(
            `An error occured. Rest assured, it will be rectified soon.`,
            PrimeNgAlerts.ERROR
          );
        } else if (
          request.url.includes('auth/token') ||
          request.url.includes('auth/refresh')
        ) {
          this.router.navigate(['/login']);
        } else {
          this.alert.showToast(
            `Something went wrong. Try again later`,
            PrimeNgAlerts.ERROR
          );
        }

        return throwError(() => event);
      })
    );
  }

  private handleTokenExpiredException() {
    if (!this.router.url.includes('login')) {
      this.alert.showToast(
        `You have been logged out. Please log in and retry`,
        PrimeNgAlerts.INFO
      );
    }
    // TODO: logout when feature is added
    this.loginService.logout();
    //.subscribe(_ => {
    this.router.navigate(['/login']);
    // this.navigator.auth.goToLogin();
    //});
  }
}
