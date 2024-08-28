import { Component, OnInit } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IStaff, IColumnDef } from '../../../shared/interfaces';
import { StaffState } from '../../../store/staff/staff.state';
import { GetStaff } from '../../../store/staff/staff.action';
import { AppAlertService } from '../../../shared/alerts/service/app-alert.service';
import { StaffFormComponent } from '../staff-form/staff-form.component';

@Component({
  selector: 'app-staff-list',
  templateUrl: './staff-list.component.html',
  styleUrls: ['./staff-list.component.scss'],
})
export class StaffListComponent implements OnInit {
  // @Select(StaffState.selectStateData) staff$!: Observable<IStaff[]>;
  staff$: Observable<IStaff[]> = this.store.select(StaffState.selectStateData);

  columns: IColumnDef[] = [
    { header: 'First Name', field: 'first_name' },
    { header: 'Last Name', field: 'last_name' },
    { header: 'Position', field: 'position' },
    { header: 'Department', field: 'department_id' },
  ];
  title = 'Staff List';
  filename: string = 'staff-list';

  constructor(public alert: AppAlertService, private store: Store) {}

  ngOnInit() {
    this.getStaff();
  }

  getStaff() {
    this.store.dispatch(new GetStaff());
  }

  addNewStaff() {
    this.alert.openDialog(StaffFormComponent, {
      header: 'Add New Staff',
      closable: true,
    });
  }
}
