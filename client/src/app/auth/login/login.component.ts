import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from '../service/login.service';
import { catchError, Observable, take } from 'rxjs';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { APP_ACCESS_TOKEN, PrimeNgAlerts } from '../../config/app-config';
import { Store } from '@ngxs/store';
import { AppState } from '../../store/app/app.state';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  loading$: Observable<boolean> = this.store.select(AppState.getLoadingState);

  userForm!: FormGroup;
  loginError = false;

  @Input() next!: string;

  constructor(
    private router: Router,
    private fb: FormBuilder,
    private loginService: LoginService,
    private alert: AppAlertService,
    private activatedRoute: ActivatedRoute,
    private store: Store
  ) {}

  ngOnInit() {
    this.userForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });

    this.activatedRoute.queryParams
      .pipe(take(1))
      .subscribe((q) => (this.next = q['next']));
  }

  ngAfterViewInit(): void {
    const accessTokenExists = localStorage.getItem(APP_ACCESS_TOKEN);
    if (accessTokenExists) {
      this.gotoNext();
    }
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
          this.gotoNext();
        }
      });
  }

  gotoNext = () => {
    return this.router.navigateByUrl(this.next ?? '/admin/dashboard');
  };
}
