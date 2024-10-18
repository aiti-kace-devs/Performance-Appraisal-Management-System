import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  OnInit,
} from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IStaff } from '../../shared/interfaces';
import { StaffState } from '../../store/staff/staff.state';
import { GetStaff } from '../../store/staff/staff.action';
import { Router } from '@angular/router';
import { StaffAppraisalState } from '../../store/appraisal/staff-appraisal.state';
import { IStaffAppraisal } from '../../shared/interfaces';
import { NavigationService } from '../../service/navigation.service';

@Component({
  selector: 'app-layout',
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.scss',
})
export class MainLayoutComponent implements OnInit, AfterViewInit {
  staff$: Observable<IStaff[]> = this.store.select(StaffState.selectStateData);

  // @Select(StaffAppraisalState.getSelectedAppraisal) selectedAppraisal$:
  //   | Observable<IStaffAppraisal>
  //   | undefined;

  selectedAppraisal$: Observable<IStaffAppraisal | null | undefined> =
    this.store.select(StaffAppraisalState.getSelectedAppraisal);

  staff: { label: any; value: any }[] = [];
  selectedStaff: any;

  breadcrumbs$ = this.navigator.breadCrumbs$;

  constructor(
    private store: Store,
    private router: Router,
    private navigator: NavigationService,
    private cdref: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.store.dispatch(new GetStaff());
    this.staff$?.subscribe((staff) => {
      this.staff = staff.map((staff) => ({
        label: staff.full_name,
        value: staff.id,
      }));
    });

    this.selectedAppraisal$?.subscribe((selectedStaff) => {
      this.selectedStaff = selectedStaff
        ? {
            label: selectedStaff.staff_info.full_name,
            value: selectedStaff.staff_info.id,
          }
        : null;
    });
    this.cdref.detectChanges();
  }

  ngAfterViewInit(): void {
    this.cdref.detectChanges();
  }

  onStaffChange(event: any) {
    this.router.navigate([
      '/admin/appraisal-management/details',
      event.value.value,
    ]);
  }
}
