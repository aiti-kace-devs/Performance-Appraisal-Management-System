import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngxs/store';
import { AppAlertService } from '../../../shared/alerts/service/app-alert.service';
import {
  AddDepartment,
  UpdateDepartment,
} from '../../../store/department/department.action';
import { catchError, finalize, of, take } from 'rxjs';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';
import { PrimeNgAlerts } from '../../../config/app-config';
import { IDepartment } from '../../../shared/interfaces';

@Component({
  selector: 'app-department-form',
  templateUrl: './department-form.component.html',
  styleUrl: './department-form.component.scss',
})
export class DepartmentFormComponent implements OnInit {
  departmentForm!: FormGroup;
  department!: IDepartment;

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
      this.department = this.config.data;

      this.departmentForm.patchValue(this.department);
    }
  }

  initializeForm() {
    this.departmentForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      description: ['', [Validators.required, Validators.minLength(3)]],
    });
  }

  submitForm() {
    if (this.departmentForm.valid) {
      let data = this.departmentForm.value;

      if (this.department?.id) {
        this.store.dispatch(new UpdateDepartment(data, this.department.id));
        this.dialogRef.close();
      } else {
        this.store
          .dispatch(new AddDepartment(data))
          .pipe(
            take(1),
            finalize(() => {
              this.dialogRef.close();
            }),
            catchError((error) => {
              this.alert.showToast(
                error.error.detail ||
                  'An error occurred while creating department.',
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
