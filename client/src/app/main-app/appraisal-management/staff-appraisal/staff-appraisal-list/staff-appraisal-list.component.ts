import { Component } from '@angular/core';
import { IColumnDef } from '../../../../shared/interfaces';

@Component({
  selector: 'app-staff-appraisal-list',
  templateUrl: './staff-appraisal-list.component.html',
  styleUrls: ['./staff-appraisal-list.component.scss'],
})
export class StaffAppraisalListComponent {
  staffData!: any;

  columns: IColumnDef[] = [
    { header: 'Staff Name', field: 'full_name', sortable: true },
    { header: 'Appraisal Type', field: 'type' },
    { header: 'Status', field: 'status', sortable: true },
  ];
  title = 'Staff Appraisal List';

  ngOnInit() {
    this.staffData = [
      { full_name: 'Rachel Green', type: 'Yearly', status: 'In Progress' },
      { full_name: 'Chandler Bing', type: 'Monthly', status: 'Completed' },
      { full_name: 'Joey Tribbiani', type: 'Yearly', status: 'In Progress' },
      { full_name: 'Ross Geller', type: 'Monthly', status: 'Completed' },
      { full_name: 'Phoebe Buffay', type: 'Yearly', status: 'In Progress' },
    ];
  }
}
