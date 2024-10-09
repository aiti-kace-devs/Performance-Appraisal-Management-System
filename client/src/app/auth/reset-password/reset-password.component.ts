import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { PrimeNgAlerts } from '../../config/app-config';
import { EMPTY, filter, skip } from 'rxjs';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss'],
})
export class ResetPasswordComponent implements OnInit {
  form!: FormGroup;
  token!: string;
  showForm = false;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    // private loginService: LoginService,
    private alert: AppAlertService,
    private router: Router
  ) {}

  ngOnInit() {
    this.getUserToken();
    this.initializeForm();
  }

  getUserToken() {
    this.route.queryParams.subscribe((params) => {
      if (params['token']) {
        this.token = params['token'];
        this.showForm = true;
      } else {
        this.alert.showToast('Token is missing', PrimeNgAlerts.ERROR);
      }
    });
  }

  initializeForm() {
    this.form = this.formBuilder.group({
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required, Validators.minLength(6)]],
    });

    this.form
      .get('confirmPassword')
      ?.valueChanges.pipe(
        filter((d) => d),
        skip(2)
      )
      .subscribe((v: string) => {
        if (v !== this.password.value) {
          this.confirmPassword.setErrors({ mismatch: true });
        } else {
          this.confirmPassword.setErrors(null);
        }
      });
  }

  get password() {
    return this.form.get('password') as FormControl;
  }

  get confirmPassword() {
    return this.form.get('confirmPassword') as FormControl;
  }

  submitPassword() {
    if (this.form.valid) {
      const data = {
        password: this.form.value.password,
      };
      // this.loginService
      //   .resetPassword(this.token, data)
      //   .pipe(
      //     catchError((er) => {
      //       this.alert.showToast(
      //         er.error.detail ??
      //           `Password reset unsuccessful. Please try again`,
      //         PrimeNgAlerts.ERROR
      //       );
      //       return EMPTY;
      //     })
      //   )
      //   .subscribe((res: any) => {
      //     this.alert.showToast(
      //       'password created successfully',
      //       PrimeNgAlerts.SUCCESS
      //     );
      //     this.router.navigate(['/']);
      //   });
    }
  }
}
