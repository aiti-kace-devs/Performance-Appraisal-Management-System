import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { tap } from 'rxjs/operators';
import { PrimeNgAlerts } from '../../config/app-config';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { KeyAreaService } from '../../main-app/appraisal-management/key-area/service/key-area.service';
import {
  AddKraBank,
  DeleteKraBank,
  GetKraBank,
  UpdateKraBank,
} from './kra-bank.action';
import { IKraBank } from '../../shared/interfaces';

export class KraBankStateModel {
  kraBank: IKraBank[];

  constructor() {
    this.kraBank = [];
  }
}

@State<KraBankStateModel>({
  name: 'kraBankState',
  defaults: {
    kraBank: [],
  },
})
@Injectable()
export class KraBankState {
  constructor(
    private kraService: KeyAreaService,
    private alert: AppAlertService
  ) {}

  @Selector()
  static selectStateData(state: KraBankStateModel) {
    return state.kraBank || [];
  }

  @Action(GetKraBank)
  getDataFromState(ctx: StateContext<KraBankStateModel>) {
    return this.kraService.getAllKras().pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          kraBank: returnData,
        });
      })
    );
  }

  @Action(AddKraBank)
  addDataToState(
    ctx: StateContext<KraBankStateModel>,
    { payload }: AddKraBank
  ) {
    return this.kraService.addKra(payload).pipe(
      tap((returnData) => {
        this.alert.showToast('Kra added successfully', PrimeNgAlerts.SUCCESS);
        const state = ctx.getState();
        ctx.patchState({
          kraBank: [...state.kraBank, returnData],
        });
      })
    );
  }

  @Action(UpdateKraBank)
  updateDataOfState(
    ctx: StateContext<KraBankStateModel>,
    { payload, id }: UpdateKraBank
  ) {
    return this.kraService.updateKra(payload, id).pipe(
      tap((returnData) => {
        this.alert.showToast('Kra edited successfully', PrimeNgAlerts.SUCCESS);
        const state = ctx.getState();

        const updatedKra = state.kraBank.map((kraBank) =>
          kraBank.id === id ? returnData : kraBank
        );

        ctx.patchState({
          kraBank: updatedKra,
        });
      })
    );
  }

  @Action(DeleteKraBank)
  deleteDataFromState(
    ctx: StateContext<KraBankStateModel>,
    { id }: DeleteKraBank
  ) {
    return this.kraService.deleteKra(id).pipe(
      tap((returnData) => {
        this.alert.showToast('Kra removed successfully', PrimeNgAlerts.SUCCESS);
        const state = ctx.getState();
        const filteredArray = state.kraBank.filter(
          (contents: any) => contents.id !== id
        );

        ctx.setState({
          ...state,
          kraBank: filteredArray,
        });
      })
    );
  }
}
