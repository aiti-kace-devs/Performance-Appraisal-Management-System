import { Component, OnInit } from '@angular/core';
import { AppAlertService } from '../../../../shared/alerts/service/app-alert.service';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IAppraisalCycle } from '../../../../shared/interfaces';
import { AppraisalCycleState } from '../../../../store/appraisal-cycle/appraisal-cycle.state';
import {
  ClearSelectedAppraisalCycle,
  DeleteAppraisalCycle,
  GetAppraisalCycle,
} from '../../../../store/appraisal-cycle/appraisal-cycle.action';
import { CycleFormDialogComponent } from '../cycle-form/cycle-form-dialog.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-appraisal-list',
  templateUrl: './appraisal-list.component.html',
  styleUrls: ['./appraisal-list.component.scss'],
})
export class AppraisalListComponent implements OnInit {
  cycle$: Observable<IAppraisalCycle[]> = this.store.select(
    AppraisalCycleState.selectStateData
  );

  constructor(
    private alert: AppAlertService,
    private store: Store,
    private router: Router
  ) {}

  ngOnInit() {
    this.store.dispatch(new ClearSelectedAppraisalCycle());
    this.getCycle();
  }

  getCycle() {
    this.store.dispatch(new GetAppraisalCycle());
  }

  addNewCycle() {
    this.alert.openDialog(CycleFormDialogComponent, {
      header: 'Add New Appraisal Cycle',
      closable: true,
    });
  }

  editCycle(data: any) {
    this.router.navigate([
      'admin/appraisal-management/configuration/',
      data.id,
    ]);
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
