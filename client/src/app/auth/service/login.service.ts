import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import {
  APP_REFRESH_TOKEN,
  APP_ACCESS_TOKEN,
  USER_INFO,
} from '../../config/app-config';
import { IAuthResponse } from '../../shared/interfaces';
import { catchError, map, of, tap } from 'rxjs';
import { Store } from '@ngxs/store';
import { LogUserOut } from '../../store/auth/auth.action';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  private authUrl = `${environment.API_URL_BASE}/auth`;
  private userUrl = `${environment.API_URL_BASE}/users`;

  constructor(private http: HttpClient, private readonly store: Store) {}

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

  forgotPassword(email: any) {
    return this.http.get(`${this.userUrl}/forgot-password/${email}`);
  }
}
