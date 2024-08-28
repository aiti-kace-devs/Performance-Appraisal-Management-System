import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { tap } from 'rxjs/operators';
import { PrimeNgAlerts } from '../../config/app-config';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { DepartmentService } from '../../main-app/department/service/department.service';
import {
  AddDepartment,
  DeleteDepartment,
  GetDepartment,
  UpdateDepartment,
} from './department.action';
import { IDepartment } from '../../shared/interfaces';

export class DepartmentStateModel {
  department: IDepartment[];

  constructor() {
    this.department = [];
  }
}

@State<DepartmentStateModel>({
  name: 'departmentState',
  defaults: {
    department: [],
  },
})
@Injectable()
export class DepartmentState {
  constructor(
    private departmentService: DepartmentService,
    private alert: AppAlertService
  ) {}

  @Selector()
  static selectStateData(state: DepartmentStateModel) {
    return state.department || [];
  }

  @Action(GetDepartment)
  getDataFromState(ctx: StateContext<DepartmentStateModel>) {
    return this.departmentService.getAllDepartment().pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          department: returnData,
        });
      })
    );
  }

  @Action(AddDepartment)
  addDataToState(
    ctx: StateContext<DepartmentStateModel>,
    { payload }: AddDepartment
  ) {
    return this.departmentService.addDepartment(payload).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Department added successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();
        ctx.patchState({
          department: [...state.department, returnData],
        });
      })
    );
  }

  @Action(UpdateDepartment)
  updateDataOfState(
    ctx: StateContext<DepartmentStateModel>,
    { payload, id }: UpdateDepartment
  ) {
    return this.departmentService.updateDepartment(payload, id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Department edited successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();

        const updatedDepartment = state.department.map((department) =>
          department.id === id ? returnData : department
        );

        ctx.patchState({
          department: updatedDepartment,
        });
      })
    );
  }

  @Action(DeleteDepartment)
  deleteDataFromState(
    ctx: StateContext<DepartmentStateModel>,
    { id }: DeleteDepartment
  ) {
    return this.departmentService.deleteDepartment(id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Department removed successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();
        const filteredArray = state.department.filter(
          (contents: any) => contents.id !== id
        );

        ctx.setState({
          ...state,
          department: filteredArray,
        });
      })
    );
  }
}
