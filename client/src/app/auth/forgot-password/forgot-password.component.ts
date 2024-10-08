import { Component } from '@angular/core';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { FormControl, Validators } from '@angular/forms';
import { PrimeNgAlerts } from '../../config/app-config';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss'],
})
export class ForgotPasswordComponent {
  constructor(
    // private loginService: LoginService,
    private alert: AppAlertService
  ) {}
  email = new FormControl('', [Validators.required, Validators.email]);

  submitForm() {
    const data = this.email.value;
    // this.loginService.forgotPassword(data).subscribe(() => {
    //   this.alert.showToast(
    //     'email submitted successfully',
    //     PrimeNgAlerts.SUCCESS
    //   );
    // });
  }
}
