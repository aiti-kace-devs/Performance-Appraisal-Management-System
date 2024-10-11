import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { LoginService } from '../../auth/service/login.service';
import { AppAlertService } from '../alerts/service/app-alert.service';
import { PrimeNgAlerts } from '../../config/app-config';

export const roleGuard: CanActivateFn = async (route, state) => {
  const loginService = inject(LoginService);
  const alertService = inject(AppAlertService);
  const router = inject(Router);

  const userRole = loginService.loggedInUser?.role;
  const allowedRoles: string[] = route.data['roles'];
  const allowed = allowedRoles.some((v) => v === userRole?.name);

  if (allowed) {
    return true;
  } else {
    alertService.showToast('You are not permitted', PrimeNgAlerts.INFO);
    router.navigateByUrl('/admin/dashboard');
    return false;
  }
};
