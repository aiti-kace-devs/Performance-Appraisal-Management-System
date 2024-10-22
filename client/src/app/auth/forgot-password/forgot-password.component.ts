import { Component } from '@angular/core';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { FormControl, Validators } from '@angular/forms';
import { PrimeNgAlerts } from '../../config/app-config';
import { LoginService } from '../service/login.service';
import { catchError, Observable } from 'rxjs';
import { AppState } from '../../store/app/app.state';
import { Store } from '@ngxs/store';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class ForgotPasswordComponent {
  loading$: Observable<boolean> = this.store.select(AppState.getLoadingState);

  constructor(
    private loginService: LoginService,
    private alert: AppAlertService,
    private store: Store
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
