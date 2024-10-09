import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../../auth/service/login.service';

@Component({
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss'],
})
export class SideBarComponent {
  constructor(private router: Router, private loginService: LoginService) {}

  logout(): any {
    if (this.loginService.logout()) {
      return this.router.navigate(['/login']);
    }
  }
}
