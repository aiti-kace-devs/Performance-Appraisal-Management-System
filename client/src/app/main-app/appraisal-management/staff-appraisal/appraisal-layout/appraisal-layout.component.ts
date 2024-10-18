import { Component, OnDestroy, OnInit } from '@angular/core';
import { StaffAppraisalState } from '../../../../store/appraisal/staff-appraisal.state';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IStaffAppraisal } from '../../../../shared/interfaces';
import { ClearSatffAppraisal } from '../../../../store/appraisal/staff-appraisal.action';

@Component({
  selector: 'app-appraisal-layout',
  templateUrl: './appraisal-layout.component.html',
  styleUrls: ['./appraisal-layout.component.scss'],
})
export class AppraisalLayoutComponent implements OnInit, OnDestroy {
  selectedAppraisal$: Observable<IStaffAppraisal | null | undefined> =
    this.store.select(StaffAppraisalState.getSelectedAppraisal);

  appraisalCycles: { name: string; description: string; sections: any }[] = [];

  constructor(private store: Store) {}

  ngOnInit() {
    this.selectedAppraisal$?.subscribe((data) => {
      if (data?.appraisal_cycles) {
        this.appraisalCycles = data.appraisal_cycles.map((app: any) => ({
          name: app.name,
          description: app.description,
          sections: app.appraisal_sections,
        }));
      }
    });
  }

  ngOnDestroy(): void {
    // this.store.dispatch(new ClearSatffAppraisal());
  }
}
