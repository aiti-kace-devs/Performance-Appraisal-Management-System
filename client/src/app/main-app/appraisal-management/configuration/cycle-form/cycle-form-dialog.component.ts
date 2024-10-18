import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DynamicDialogRef } from 'primeng/dynamicdialog';

@Component({
  selector: 'app-cycle-form-dialog',
  template: `<app-cycle-form
    (cycleAdded)="closeDialog($event)"
  ></app-cycle-form>`,
})
export class CycleFormDialogComponent {
  /**
   *
   */
  constructor(private dialogRef: DynamicDialogRef, private router: Router) {}

  closeDialog(id: any) {
    this.dialogRef.close();
    this.router.navigate(['/admin/appraisal-management/configuration', id], {
      queryParams: { index: 0 },
    });
  }
}
