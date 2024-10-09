import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';
import { LoginService } from '../service/login.service';
import { catchError } from 'rxjs';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { PrimeNgAlerts } from '../../config/app-config';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  userForm!: FormGroup;
  loginError = false;

  constructor(
    private router: Router,
    private fb: FormBuilder,
    private loginService: LoginService,
    private alert: AppAlertService
  ) {}

  ngOnInit() {
    this.userForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  login() {
    const credentials = new FormData();
    credentials.append('username', this.userForm.value.email);
    credentials.append('password', this.userForm.value.password);
    this.loginService
      .login(credentials)
      .pipe(
        catchError((error: any) => {
          this.loginError = true;
          return error;
        })
      )
      .subscribe((result: any) => {
        if (result) {
          this.alert.showToast('Log in successful', PrimeNgAlerts.UNOBSTRUSIVE);
          this.router.navigate(['/admin/dashboard']);
        }
      });
  }
}
