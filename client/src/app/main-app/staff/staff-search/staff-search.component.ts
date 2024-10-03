import { Component, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Store } from '@ngxs/store';
import { StaffState } from '../../../store/staff/staff.state';
import { Observable } from 'rxjs';
import { IStaff } from '../../../shared/interfaces';
import { GetStaff } from '../../../store/staff/staff.action';
import { AutoCompleteCompleteEvent } from 'primeng/autocomplete';

@Component({
  selector: 'app-staff-search',
  templateUrl: './staff-search.component.html',
  styleUrls: ['./staff-search.component.scss'],
})
export class StaffSearchComponent implements OnInit {
  @Input()
  control!: FormControl;

  staff$: Observable<IStaff[]> = this.store.select(StaffState.selectStateData);
  staffs: IStaff[] = [];
  filteredStaffs: IStaff[] = [];

  constructor(private store: Store) {}

  ngOnInit(): void {
    this.store.dispatch(new GetStaff());

    this.staff$.subscribe((staffs) => {
      this.staffs = staffs;
    });
  }

  staffSearchFunction(event: AutoCompleteCompleteEvent) {
    const query = event.query.toLowerCase();
    this.filteredStaffs = this.staffs.filter((staff) =>
      staff.full_name?.toLowerCase().includes(query)
    );
  }
}
