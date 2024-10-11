import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../../auth/service/login.service';
import { AuthState } from '../../store/auth/auth.state';
import { Observable } from 'rxjs';
import { IUser } from '../../shared/interfaces';
import { Select } from '@ngxs/store';

@Component({
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss'],
})
export class SideBarComponent {
  @Select(AuthState.getLoggedInUser) user$: Observable<IUser> | undefined;

  constructor(private router: Router, private loginService: LoginService) {}

  logout(): any {
    if (this.loginService.logout()) {
      return this.router.navigate(['/login']);
    }
  }
}
