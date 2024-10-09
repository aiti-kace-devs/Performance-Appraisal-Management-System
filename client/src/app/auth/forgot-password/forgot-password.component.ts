import { Component } from '@angular/core';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { FormControl, Validators } from '@angular/forms';
import { PrimeNgAlerts } from '../../config/app-config';
import { LoginService } from '../service/login.service';
import { catchError } from 'rxjs';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class ForgotPasswordComponent {
  constructor(
    private loginService: LoginService,
    private alert: AppAlertService
  ) {}
  email = new FormControl('', [Validators.required, Validators.email]);

  submitForm() {
    const data = this.email.value;
    this.loginService
      .forgotPassword(data)
      .pipe(
        catchError((error) => {
          this.alert.showToast(
            error.error.detail ?? 'Error while submitting email',
            PrimeNgAlerts.ERROR
          );
          return error;
        })
      )
      .subscribe(() => {
        this.alert.showToast(
          'email submitted successfully',
          PrimeNgAlerts.UNOBSTRUSIVE
        );
      });
  }
}
