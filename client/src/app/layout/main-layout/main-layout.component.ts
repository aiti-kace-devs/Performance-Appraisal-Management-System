import {
  AfterViewInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  OnInit,
} from '@angular/core';
import { Store } from '@ngxs/store';
import { BehaviorSubject, Observable } from 'rxjs';
import { IStaff } from '../../shared/interfaces';
import { StaffState } from '../../store/staff/staff.state';
import { GetStaff } from '../../store/staff/staff.action';
import { Router } from '@angular/router';
import { StaffAppraisalState } from '../../store/appraisal/staff-appraisal.state';
import { IStaffAppraisal } from '../../shared/interfaces';
import { NavigationService } from '../../service/navigation.service';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
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

  breadcrumbs$: BehaviorSubject<MenuItem[]> = this.navigator.breadCrumbs$;

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
  }

  ngAfterViewInit(): void {
    this.breadcrumbs$.subscribe(() => {
      this.cdref.detectChanges();
    });
  }

  onStaffChange(event: any) {
    this.router.navigate([
      '/admin/appraisal-management/details',
      event.value.value,
    ]);
  }
}
