import { Component } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IStaff } from '../../shared/interfaces';
import { StaffState } from '../../store/staff/staff.state';
import { GetStaff } from '../../store/staff/staff.action';
import { Router } from '@angular/router';

@Component({
  selector: 'app-layout',
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.scss',
})
export class MainLayoutComponent {
  staff$: Observable<IStaff[]> = this.store.select(StaffState.selectStateData);
  // hideOnOutsideClick: boolean = true;
  staff: { label: any; value: any }[] = [];
  selectedStaff: any;

  constructor(private store: Store, private router: Router) {}

  ngOnInit() {
    this.store.dispatch(new GetStaff());
    this.staff$?.subscribe((staff) => {
      this.staff = staff.map((staff) => ({
        label: staff.full_name,
        value: staff.id,
      }));
    });
  }

  onStaffChange(event: any) {
    this.router.navigate([
      '/admin/appraisal-management/details',
      event.value.value,
    ]);
  }
}
