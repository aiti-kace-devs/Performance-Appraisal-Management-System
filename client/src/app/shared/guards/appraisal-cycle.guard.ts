import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Store } from '@ngxs/store';
import { catchError, of, switchMap } from 'rxjs';
import { SelectAppraisalCycle } from '../../store/appraisal-cycle/appraisal-cycle.action';

export const appraisalCycleGuard: CanActivateFn = (route, state) => {
  const cycle_id = route.params['cycle_id'];
  const store = inject(Store);

  if (cycle_id) {
    return store.dispatch(new SelectAppraisalCycle(cycle_id)).pipe(
      catchError((err) => {
        return of(false);
      }),
      switchMap(() => of(true))
    );
  }
  return true;
};
