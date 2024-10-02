import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { Store } from '@ngxs/store';
import { catchError, finalize, Observable, of, take, tap } from 'rxjs';
import { DepartmentState } from '../../../store/department/department.state';
import { IDepartment } from '../../../shared/interfaces';
import { GetDepartment } from '../../../store/department/department.action';
import { AutoCompleteCompleteEvent } from 'primeng/autocomplete';
import { RolesService } from '../../roles/service/roles.service';
import { ISODate, PrimeNgAlerts } from '../../../config/app-config';
import { DynamicDialogConfig, DynamicDialogRef } from 'primeng/dynamicdialog';
import { AppAlertService } from '../../../shared/alerts/service/app-alert.service';
import { AddStaff, UpdateStaff } from '../../../store/staff/staff.action';

interface IDropdown {
  label: string;
  value: string;
}

@Component({
  selector: 'app-staff-form',
  templateUrl: './staff-form.component.html',
  styleUrls: ['./staff-form.component.scss'],
})
export class StaffFormComponent implements OnInit {
  readOnly: boolean = false;
  staffForm!: FormGroup;
  staff!: any;

  department$: Observable<IDepartment[]> = this.store.select(
    DepartmentState.selectStateData
  );

  departments: IDepartment[] = [];
  filteredDepartments: IDepartment[] = [];

  titleArray = [
    'Mr.',
    'Prof.',
    'Miss',
    'Mrs.',
    'Ing.',
    'Dr.',
    'Rev.',
    'Rev.Dr.',
    'Bishop',
    'Other',
  ];
  titles: IDropdown[] = [];
  gender: IDropdown[] = [];
  roles = [];

  constructor(
    private formBuilder: FormBuilder,
    private store: Store,
    private roleService: RolesService,
    private alert: AppAlertService,
    private dialogRef: DynamicDialogRef,
    private config: DynamicDialogConfig
  ) {}

  ngOnInit() {
    this.titles = this.titleArray.map((t) => {
      return { label: t, value: t };
    });

    this.gender = [
      { label: 'Male', value: 'Male' },
      { label: 'Female', value: 'Female' },
    ];

    this.store.dispatch(new GetDepartment());

    this.department$.subscribe((departments) => {
      this.departments = departments;
    });

    this.roleService.getAllRoles().subscribe((d: any) => {
      this.roles = d.filter(
        (role: any) => role.name.toLowerCase() !== 'super admin'
      );
    });

    this.initializeForm();
  }

  ngAfterViewInit(): void {
    if (this.config.data?.id) {
      this.readOnly = this.config.data?.type === 'view';
      this.staff = this.config.data;
      const role = this.staff.role_id.id;
      const appointment = new Date(Date.parse(this.staff.appointment_date));

      this.staffForm.patchValue({
        ...this.staff,
        appointment_date: appointment,
        role_id: role,
      });
    }
  }

  initializeForm() {
    this.staffForm = this.formBuilder.group({
      title: ['', [Validators.required, Validators.minLength(2)]],
      first_name: ['', [Validators.required, Validators.minLength(3)]],
      last_name: ['', [Validators.required, Validators.minLength(3)]],
      other_name: ['', [Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      gender: ['', [Validators.required]],
      department_id: ['', [Validators.required]],
      position: ['', [Validators.required]],
      grade: ['', [Validators.required]],
      appointment_date: ['', [Validators.required]],
      role_id: [],
    });
  }

  filterDepartment(event: AutoCompleteCompleteEvent) {
    const query = event.query.toLowerCase();
    this.filteredDepartments = this.departments.filter((department) =>
      department.name.toLowerCase().includes(query)
    );
  }

  submitForm() {
    // if (this.staffForm.valid) {
    let data = this.staffForm.value;
    data['department_id'] = data.department_id.id;
    data['appointment_date'] = ISODate(data.appointment_date);
    // console.log(data);

    if (this.staff?.id) {
      this.store.dispatch(new UpdateStaff(data, this.staff.id));
      this.dialogRef.close();
    } else {
      this.store
        .dispatch(new AddStaff(data))
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

    // }
  }
}
