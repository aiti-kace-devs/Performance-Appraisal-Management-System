import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { lastValueFrom } from 'rxjs';
import { LoginService } from '../../auth/service/login.service';
import { AuthState } from '../../store/auth/auth.state';

export const authGuard: CanActivateFn = async (route, state) => {
  const store = inject(Store);
  const router = inject(Router);
  const loginService = inject(LoginService);

  const url = state.url;

  const loggedInUser = await lastValueFrom(
    store.selectOnce(AuthState.getLoggedInUser)
  );

  if (loggedInUser) {
    return true;
  } else {
    const tokenRefreshed = await lastValueFrom(
      loginService.requestNewAccessToken()
    );

    if (tokenRefreshed) {
      return true;
    } else {
      router.navigate(['/login'], { queryParams: { next: url } });
      return false;
    }
  }
};
