import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Store } from '@ngxs/store';
import { SelectSatffAppraisal } from '../../store/appraisal/staff-appraisal.action';
import { catchError, of, switchMap } from 'rxjs';

export const staffAppraisalGuard: CanActivateFn = (route, state) => {
  const staff_id = route.params['staff_id'];
  const store = inject(Store);

  if (staff_id) {
    return store.dispatch(new SelectSatffAppraisal(staff_id)).pipe(
      catchError((err) => {
        return of(false);
      }),
      switchMap(() => of(true))
    );
  }
  return true;
};
