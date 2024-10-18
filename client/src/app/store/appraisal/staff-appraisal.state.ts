import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { tap } from 'rxjs/operators';
import {
  SelectSatffAppraisal,
  ClearSatffAppraisal,
} from './staff-appraisal.action';
import { IStaffAppraisal } from '../../shared/interfaces';
import { StaffAppraisalService } from '../../main-app/appraisal-management/staff-appraisal/service/staff-appraisal.service';

export class StaffAppraisalStateModel {
  selectedStaffAppraisal: IStaffAppraisal | undefined | null;

  constructor() {
    this.selectedStaffAppraisal = undefined;
  }
}

@State<StaffAppraisalStateModel>({
  name: 'staffAppraisalState',
  defaults: {
    selectedStaffAppraisal: undefined,
  },
})
@Injectable()
export class StaffAppraisalState {
  constructor(private appraisalService: StaffAppraisalService) {}

  @Selector()
  static getSelectedAppraisal(state: StaffAppraisalStateModel) {
    return state.selectedStaffAppraisal;
  }

  @Action(SelectSatffAppraisal)
  selectSatffAppraisal(
    ctx: StateContext<StaffAppraisalStateModel>,
    { id }: SelectSatffAppraisal
  ) {
    return this.appraisalService.getStaffAppraisal(id).pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          selectedStaffAppraisal: returnData,
        });
      })
    );
  }

  @Action(ClearSatffAppraisal)
  clearSatffAppraisal(ctx: StateContext<StaffAppraisalStateModel>) {
    // ctx.patchState({ selectedStaffAppraisal: undefined });
    return ctx.setState({
      selectedStaffAppraisal: undefined,
    });
  }
}
