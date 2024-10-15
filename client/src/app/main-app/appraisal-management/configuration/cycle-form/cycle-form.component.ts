import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngxs/store';
import { AppAlertService } from '../../../../shared/alerts/service/app-alert.service';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';
import { IAppraisalCycle } from '../../../../shared/interfaces';
import {
  AddAppraisalCycle,
  UpdateAppraisalCycle,
} from '../../../../store/appraisal-cycle/appraisal-cycle.action';
import { catchError, finalize, of, take } from 'rxjs';
import { PrimeNgAlerts } from '../../../../config/app-config';

@Component({
  selector: 'app-cycle-form',
  templateUrl: './cycle-form.component.html',
  styleUrls: ['./cycle-form.component.scss'],
})
export class CycleFormComponent implements OnInit {
  cycleForm!: FormGroup;
  appraisalCycle!: IAppraisalCycle;

  constructor(
    private formBuilder: FormBuilder,
    private store: Store,
    private alert: AppAlertService,
    private dialogRef: DynamicDialogRef,
    private config: DynamicDialogConfig
  ) {}
  ngOnInit() {
    this.initializeForm();
  }

  ngAfterViewInit(): void {
    if (this.config.data?.id) {
      this.appraisalCycle = this.config.data;

      this.cycleForm.patchValue(this.appraisalCycle);
    }
  }

  initializeForm() {
    this.cycleForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      description: ['', [Validators.required, Validators.minLength(3)]],
    });
  }

  submitForm() {
    if (this.cycleForm.valid) {
      let data = this.cycleForm.value;

      if (this.appraisalCycle?.id) {
        this.store.dispatch(
          new UpdateAppraisalCycle(data, this.appraisalCycle.id)
        );
        this.dialogRef.close();
      } else {
        this.store
          .dispatch(new AddAppraisalCycle(data))
          .pipe(
            take(1),
            finalize(() => {
              this.dialogRef.close();
            }),
            catchError((error) => {
              this.alert.showToast(
                error.error.detail ||
                  'An error occurred while creating appraisal cycle.',
                PrimeNgAlerts.ERROR
              );
              return of(null);
            })
          )
          .subscribe();
      }
    }
  }
}
