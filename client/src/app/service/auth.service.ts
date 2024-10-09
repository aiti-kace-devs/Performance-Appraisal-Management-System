import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { APP_ACCESS_TOKEN } from '../config/app-config';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  public getToken(): string {
    return localStorage.getItem(APP_ACCESS_TOKEN) || '';
  }

  jwtHelper: JwtHelperService = new JwtHelperService();
  // ...
  public isAuthenticated(): boolean {
    const token = this.getToken(); // Check whether the token is expired and return
    // true or false
    return !this.jwtHelper.isTokenExpired(token);
  }
}
