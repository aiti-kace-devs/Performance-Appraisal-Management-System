import { Component, OnInit } from '@angular/core';
import { AppAlertService } from '../../../../shared/alerts/service/app-alert.service';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IAppraisalCycle } from '../../../../shared/interfaces';
import { AppraisalCycleState } from '../../../../store/appraisal-cycle/appraisal-cycle.state';
import {
  DeleteAppraisalCycle,
  GetAppraisalCycle,
} from '../../../../store/appraisal-cycle/appraisal-cycle.action';
import { CycleFormComponent } from '../cycle-form/cycle-form.component';

@Component({
  selector: 'app-appraisal-list',
  templateUrl: './appraisal-list.component.html',
  styleUrls: ['./appraisal-list.component.scss'],
})
export class AppraisalListComponent implements OnInit {
  cycle$: Observable<IAppraisalCycle[]> = this.store.select(
    AppraisalCycleState.selectStateData
  );

  constructor(public alert: AppAlertService, private store: Store) {}

  ngOnInit() {
    this.getCycle();
  }

  getCycle() {
    this.store.dispatch(new GetAppraisalCycle());
  }

  addNewCycle() {
    this.alert.openDialog(CycleFormComponent, {
      header: 'Add New Appraisal Cycle',
      closable: true,
    });
  }

  editCycle(data: any) {
    this.alert.openDialog(CycleFormComponent, {
      header: 'Update Appraisal Cycle',
      data: data,
      closable: true,
    });
  }
  removeCycle(data: any) {
    this.alert.showConfirmation({
      popupTarget: event?.target,
      message: 'Are you sure you want to proceed?',
      acceptFunction: () => {
        this.store.dispatch(new DeleteAppraisalCycle(data.id));
      },
    });
  }
}
