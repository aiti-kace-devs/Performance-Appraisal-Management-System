import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { tap } from 'rxjs/operators';
import { PrimeNgAlerts } from '../../config/app-config';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { StaffService } from '../../main-app/staff/service/staff.service';
import { AddStaff, DeleteStaff, GetStaff, UpdateStaff } from './staff.action';
import { IStaff } from '../../shared/interfaces';

export class StaffStateModel {
  staff: IStaff[];

  constructor() {
    this.staff = [];
  }
}

@State<StaffStateModel>({
  name: 'staffState',
  defaults: {
    staff: [],
  },
})
@Injectable()
export class StaffState {
  constructor(
    private staffService: StaffService,
    private alert: AppAlertService
  ) {}

  @Selector()
  static selectStateData(state: StaffStateModel) {
    return state.staff || [];
  }

  @Action(GetStaff)
  getDataFromState(ctx: StateContext<StaffStateModel>) {
    return this.staffService.getAllStaff().pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          staff: returnData,
        });
      })
    );
  }

  @Action(AddStaff)
  addDataToState(ctx: StateContext<StaffStateModel>, { payload }: AddStaff) {
    return this.staffService.addStaff(payload).pipe(
      tap((returnData) => {
        this.alert.showToast('Staff added successfully', PrimeNgAlerts.SUCCESS);
        const state = ctx.getState();
        ctx.patchState({
          staff: [...state.staff, returnData],
        });
      })
    );
  }

  @Action(UpdateStaff)
  updateDataOfState(
    ctx: StateContext<StaffStateModel>,
    { payload, id }: UpdateStaff
  ) {
    return this.staffService.updateStaff(payload, id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Staff edited successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();

        const updatedStaff = state.staff.map((staff) =>
          staff.id === id ? returnData : staff
        );

        ctx.patchState({
          staff: updatedStaff,
        });
      })
    );
  }

  @Action(DeleteStaff)
  deleteDataFromState(ctx: StateContext<StaffStateModel>, { id }: DeleteStaff) {
    return this.staffService.deleteStaff(id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'user removed successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();
        const filteredArray = state.staff.filter(
          (contents: any) => contents.id !== id
        );

        ctx.setState({
          ...state,
          staff: filteredArray,
        });
      })
    );
  }
}
