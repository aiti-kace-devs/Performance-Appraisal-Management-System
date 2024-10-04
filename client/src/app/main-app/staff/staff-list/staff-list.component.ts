import { Component, OnInit } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable, of } from 'rxjs';
import { IStaff, IColumnDef } from '../../../shared/interfaces';
import { StaffState } from '../../../store/staff/staff.state';
import { DeleteStaff, GetStaff } from '../../../store/staff/staff.action';
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
    { header: 'Full Name', field: 'full_name', sortable: true },
    { header: 'Position', field: 'position' },
    { header: 'Supervisor', field: 'supervisor_id', subField: 'full_name' },
    { header: 'Department', field: 'department_id', subField: 'name' },
  ];
  title = 'Staff List';
  filename: string = 'staff-list';
  staffs: IStaff[] = [];

  constructor(public alert: AppAlertService, private store: Store) {}

  ngOnInit() {
    this.getStaff();

    this.staff$.subscribe((staff) => {
      this.staffs = staff;
    });
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

  viewStaff(data: any) {
    this.alert.openDialog(StaffFormComponent, {
      header: 'Staff Details',
      data: { ...data, type: 'view' },
      closable: true,
    });
  }

  editStaff(data: any) {
    this.alert.openDialog(StaffFormComponent, {
      header: 'Update Staff Details',
      data: { ...data, type: 'edit' },
      closable: true,
    });
  }

  removeStaff(data: any) {
    this.alert.showConfirmation({
      popupTarget: event?.target,
      message: 'Are you sure you want to proceed?',
      acceptFunction: () => {
        this.store.dispatch(new DeleteStaff(data.id));
      },
    });
  }

  searchFunction = (toSearch: string) => {
    const filtered = this.staffs?.filter((d) => {
      return d.full_name?.toLowerCase().includes(toSearch);
    });

    return of(filtered || []);
  };
}
