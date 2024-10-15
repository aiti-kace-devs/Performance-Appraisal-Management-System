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

  appraisalSections: { name: string; description: string; formData: any }[] =
    [];

  constructor(private store: Store) {}

  ngOnInit() {
    this.selectedAppraisal$?.subscribe((data) => {
      if (data?.data) {
        this.appraisalSections = data.data.map((section: any) => ({
          name: section.appraisal_section.name,
          description: section.appraisal_section.description,
          formData: section.appraisal_form,
        }));
      }
    });
  }

  ngOnDestroy(): void {
    // this.store.dispatch(new ClearSatffAppraisal());
  }
}
