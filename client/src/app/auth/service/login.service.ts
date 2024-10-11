import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import {
  APP_REFRESH_TOKEN,
  APP_ACCESS_TOKEN,
  USER_INFO,
} from '../../config/app-config';
import { IAuthResponse, IUser } from '../../shared/interfaces';
import { catchError, map, of, retry, switchMap, tap } from 'rxjs';
import { Store } from '@ngxs/store';
import { LogUserOut, SetLogggedInUser } from '../../store/auth/auth.action';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  private authUrl = `${environment.API_URL_BASE}/auth`;
  private userUrl = `${environment.API_URL_BASE}/users`;

  constructor(private http: HttpClient, private readonly store: Store) {}

  loggedInUser: IUser | undefined;

  login = (user: any) => {
    return this.http.post<IAuthResponse>(`${this.authUrl}/token`, user).pipe(
      tap(() => localStorage.clear()),
      map((response: IAuthResponse) => {
        if (response.user) {
          localStorage.setItem(APP_REFRESH_TOKEN, response.refresh_token);
          localStorage.setItem(APP_ACCESS_TOKEN, response.access_token);
          localStorage.setItem(USER_INFO, JSON.stringify(response.user));
          return true;
        } else {
          return false;
        }
      }),
      catchError((e) => of(false))
    );
  };

  logout = () => {
    localStorage.clear();
    this.store.dispatch(new LogUserOut());
    return true;
  };

  requestNewAccessToken = (token?: string) => {
    const refreshToken = token
      ? token
      : localStorage.getItem(APP_REFRESH_TOKEN);
    return this.http
      .post<IAuthResponse>(`${this.authUrl}/refresh`, {
        refresh_token: refreshToken,
      })
      .pipe(
        switchMap((response: IAuthResponse) => {
          if (response.access_token) {
            localStorage.clear();
            localStorage.setItem(APP_REFRESH_TOKEN, response.refresh_token);
            localStorage.setItem(APP_ACCESS_TOKEN, response.access_token);
            return this.getMyDetails().pipe(
              catchError(() => {
                this.logout();
                return of(false);
              }),
              map((user) => {
                if (user) {
                  this.store.dispatch(new SetLogggedInUser(user as any));
                  return true;
                }
                return false;
              })
            );
          } else {
            return of(false);
          }
        }),
        catchError((e) => of(false))
      );
  };

  getMyDetails = () => {
    const accessToken = localStorage.getItem(APP_ACCESS_TOKEN);
    const refreshToken = localStorage.getItem(APP_REFRESH_TOKEN);

    if (!accessToken && !refreshToken) {
      return of(undefined);
    }

    return this.http
      .post<IUser>(`${this.authUrl}/me`, {
        access_token: accessToken,
      })
      .pipe(
        map((user: IUser) => {
          this.loggedInUser = user;
          this.store.dispatch(new SetLogggedInUser(user));
          // if (user?.role?.name.toLowerCase() === 'super_admin') {
          //   this.store.dispatch(new SetModeratorType('ADMIN'));
          // }
          return user;
        }),
        retry(1),
        catchError((e) => of(undefined))
      );
  };

  forgotPassword(email: any) {
    return this.http.get(`${this.userUrl}/forgot-password/${email}`);
  }

  resetPassword(token: string, data: any) {
    return this.http.put(`${this.userUrl}/reset-password-token/${token}`, data);
  }
}
