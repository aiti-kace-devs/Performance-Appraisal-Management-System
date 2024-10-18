import { Component } from '@angular/core';
import { IColumnDef, IStaff } from '../../../../shared/interfaces';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { StaffState } from '../../../../store/staff/staff.state';
import { GetStaff } from '../../../../store/staff/staff.action';

@Component({
  selector: 'app-staff-appraisal-list',
  templateUrl: './staff-appraisal-list.component.html',
  styleUrls: ['./staff-appraisal-list.component.scss'],
})
export class StaffAppraisalListComponent {
  staff$: Observable<IStaff[]> = this.store.select(StaffState.selectStateData);
  staffData!: any;

  columns: IColumnDef[] = [
    { header: 'Staff Name', field: 'full_name', sortable: true },
    { header: 'Position', field: 'position' },
    {
      header: 'Department',
      field: 'department_id',
      subField: 'name',
    },
  ];
  title = 'Staff Appraisal List';

  constructor(private store: Store) {}

  ngOnInit() {
    this.store.dispatch(new GetStaff());
  }
}
