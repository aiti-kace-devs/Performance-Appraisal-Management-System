import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { tap } from 'rxjs/operators';
import { PrimeNgAlerts } from '../../config/app-config';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { ConfigurationService } from '../../main-app/appraisal-management/configuration/service/configuration.service';
import {
  AddAppraisalCycle,
  DeleteAppraisalCycle,
  GetAppraisalCycle,
  UpdateAppraisalCycle,
  SelectAppraisalCycle,
  ClearSelectedAppraisalCycle,
} from './appraisal-cycle.action';
import { IAppraisalCycle } from '../../shared/interfaces';

export class AppraisalCycleStateModel {
  cycle: IAppraisalCycle[];
  selectedCycle: any;

  constructor() {
    this.cycle = [];
    this.selectedCycle = undefined;
  }
}

@State<AppraisalCycleStateModel>({
  name: 'appraisalCycleState',
  defaults: {
    cycle: [],
    selectedCycle: undefined,
  },
})
@Injectable()
export class AppraisalCycleState {
  constructor(
    private confService: ConfigurationService,
    private alert: AppAlertService
  ) {}

  @Selector()
  static selectStateData(state: AppraisalCycleStateModel) {
    return state.cycle;
  }

  @Selector()
  static getSelectedCycle(state: AppraisalCycleStateModel) {
    return state.selectedCycle;
  }

  // @Selector()
  // static getSelectedCycleSettings(state: AppraisalCycleStateModel) {
  //   return state.selectedCycle?.settings?.settings;
  // }

  @Action(GetAppraisalCycle)
  getDataFromState(ctx: StateContext<AppraisalCycleStateModel>) {
    return this.confService.getAllCycle().pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          cycle: returnData,
        });
      })
    );
  }

  @Action(AddAppraisalCycle)
  addDataToState(
    ctx: StateContext<AppraisalCycleStateModel>,
    { payload }: AddAppraisalCycle
  ) {
    return this.confService.addCycle(payload).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Appraisal Cycle added successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();
        ctx.patchState({
          cycle: [...state.cycle, returnData],
        });
      })
    );
  }

  @Action(UpdateAppraisalCycle)
  updateDataOfState(
    ctx: StateContext<AppraisalCycleStateModel>,
    { payload, id }: UpdateAppraisalCycle
  ) {
    return this.confService.updateCycle(payload, id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Appraisal Cycle edited successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();

        const updatedCycle = state.cycle.map((cycle) =>
          cycle.id === id ? returnData : cycle
        );

        ctx.patchState({
          cycle: updatedCycle,
        });
      })
    );
  }

  @Action(DeleteAppraisalCycle)
  deleteDataFromState(
    ctx: StateContext<AppraisalCycleStateModel>,
    { id }: DeleteAppraisalCycle
  ) {
    return this.confService.deleteCycle(id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Cycle removed successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();
        const filteredArray = state.cycle.filter(
          (contents: any) => contents.id !== id
        );

        ctx.setState({
          ...state,
          cycle: filteredArray,
        });
      })
    );
  }

  @Action(SelectAppraisalCycle)
  selectAppraisalCycle(
    ctx: StateContext<AppraisalCycleStateModel>,
    { id }: SelectAppraisalCycle
  ) {
    return this.confService.getCycleWithSections(id).pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          selectedCycle: returnData,
        });
      })
    );
  }

  @Action(ClearSelectedAppraisalCycle)
  clearApprasialCycle(ctx: StateContext<AppraisalCycleStateModel>) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      selectedCycle: undefined,
    });
  }
}
