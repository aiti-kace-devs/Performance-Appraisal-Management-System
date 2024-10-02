import { Component } from '@angular/core';
import { IColumnDef } from '../../../shared/interfaces';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { DepartmentState } from '../../../store/department/department.state';
import {
  ClearDepartmentMembers,
  GetDepartmentMembers,
} from '../../../store/department/department.action';
import { DynamicDialogConfig } from 'primeng/dynamicdialog';

@Component({
  selector: 'app-department-members',
  templateUrl: './department-members.component.html',
  styleUrl: './department-members.component.scss',
})
export class DepartmentMembersComponent {
  staff$: Observable<any[]> = this.store.select(
    DepartmentState.selectDepartmentMembers
  );
  department_id: string = '';

  columns: IColumnDef[] = [{ header: 'Staff Name', field: 'full_name' }];

  constructor(private store: Store, private config: DynamicDialogConfig) {}

  ngOnInit() {
    if (this.config.data?.id) {
      this.department_id = this.config.data.id;
    }
    this.getDepartment();
  }

  getDepartment() {
    this.store.dispatch(new GetDepartmentMembers(this.department_id));
  }

  ngOnDestroy() {
    this.store.dispatch(new ClearDepartmentMembers());
  }
}
