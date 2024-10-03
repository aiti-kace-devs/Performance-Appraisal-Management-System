import { Injectable } from '@angular/core';
import { AbstractControl, AsyncValidatorFn } from '@angular/forms';
import { of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { StaffService } from '../main-app/staff/service/staff.service';

@Injectable({
  providedIn: 'root',
})
export class CustomValidators {
  /**
   *
   */
  constructor(private staffService: StaffService) {}

  emailExists = (userEmail: string | null): AsyncValidatorFn => {
    return (control: AbstractControl) => {
      if (
        userEmail &&
        control.value &&
        userEmail.toLocaleLowerCase() === control.value.toLocaleLowerCase()
      ) {
        return of(null);
      }

      return this.staffService.userEmailExists(control.value).pipe(
        catchError(() => of({ emailExists: true })),
        map((exists) => {
          return exists ? { emailExists: true } : null;
        })
      );
    };
  };
}
