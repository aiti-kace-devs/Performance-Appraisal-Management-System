import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { catchError, map, tap } from 'rxjs/operators';
import { PrimeNgAlerts } from '../../config/app-config';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { DepartmentService } from '../../main-app/department/service/department.service';
import {
  AddDepartment,
  DeleteDepartment,
  GetDepartment,
  UpdateDepartment,
  GetDepartmentMembers,
  ClearDepartmentMembers,
} from './department.action';
import { IDepartment } from '../../shared/interfaces';
import { EMPTY } from 'rxjs';

export class DepartmentStateModel {
  department: IDepartment[];
  departmentList: any;

  constructor() {
    this.department = [];
    this.departmentList = [];
  }
}

@State<DepartmentStateModel>({
  name: 'departmentState',
  defaults: {
    department: [],
    departmentList: [],
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

  @Selector()
  static selectDepartmentMembers(state: DepartmentStateModel) {
    return state.departmentList || [];
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
      catchError((err) => {
        this.alert.showToast(
          err.error.detail ?? 'Unable to delete department',
          PrimeNgAlerts.ERROR
        );
        return EMPTY;
      }),
      map((returnData) => {
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

  @Action(GetDepartmentMembers)
  getDepartmentMembers(
    ctx: StateContext<DepartmentStateModel>,
    { id }: GetDepartmentMembers
  ) {
    return this.departmentService.getDepartmentMembers(id).pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          departmentList: returnData,
        });
      })
    );
  }

  @Action(ClearDepartmentMembers)
  clearDepartmentMembers(ctx: StateContext<DepartmentStateModel>) {
    ctx.patchState({ departmentList: [] });
  }
}
