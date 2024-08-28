import { Component, OnInit } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IDepartment, IColumnDef } from '../../../shared/interfaces';
import { DepartmentState } from '../../../store/department/department.state';
import {
  DeleteDepartment,
  GetDepartment,
} from '../../../store/department/department.action';
import { AppAlertService } from '../../../shared/alerts/service/app-alert.service';
import { DepartmentFormComponent } from '../department-form/department-form.component';

@Component({
  selector: 'app-department-list',
  templateUrl: './department-list.component.html',
  styleUrl: './department-list.component.scss',
})
export class DepartmentListComponent implements OnInit {
  department$: Observable<IDepartment[]> = this.store.select(
    DepartmentState.selectStateData
  );

  columns: IColumnDef[] = [
    { header: 'Department Name', field: 'name' },
    { header: 'Description', field: 'description' },
  ];
  title = 'Department List';
  filename: string = 'department-list';

  constructor(public alert: AppAlertService, private store: Store) {}

  ngOnInit() {
    this.getDepartment();
  }

  getDepartment() {
    this.store.dispatch(new GetDepartment());
  }

  addNewDepartment() {
    this.alert.openDialog(DepartmentFormComponent, {
      header: 'Add New Department',
      closable: true,
    });
  }

  editDepartment(data: any) {
    this.alert.openDialog(DepartmentFormComponent, {
      header: 'Update Department',
      data: data,
      closable: true,
    });
  }

  removeDepartment(data: any) {
    this.alert.showConfirmation({
      popupTarget: event?.target,
      message: 'Are you sure you want to proceed?',
      acceptFunction: () => {
        this.store.dispatch(new DeleteDepartment(data.id));
      },
    });
  }
}
