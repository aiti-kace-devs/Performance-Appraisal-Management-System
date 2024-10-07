import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { tap } from 'rxjs/operators';
import { PrimeNgAlerts } from '../../config/app-config';
import { AppAlertService } from '../../shared/alerts/service/app-alert.service';
import { CompetencyBankService } from '../../main-app/appraisal-management/competency-bank/service/competency-bank.service';
import {
  AddCompetencyBank,
  DeleteCompetencyBank,
  GetCompetencyBank,
  UpdateCompetencyBank,
} from './competency-bank.action';
import { ICompetencyBank } from '../../shared/interfaces';

export class CompetencyBankStateModel {
  competencyBank: ICompetencyBank[];

  constructor() {
    this.competencyBank = [];
  }
}

@State<CompetencyBankStateModel>({
  name: 'competencyBankState',
  defaults: {
    competencyBank: [],
  },
})
@Injectable()
export class CompetencyBankState {
  constructor(
    private competencyService: CompetencyBankService,
    private alert: AppAlertService
  ) {}

  @Selector()
  static selectStateData(state: CompetencyBankStateModel) {
    return state.competencyBank || [];
  }

  @Action(GetCompetencyBank)
  getDataFromState(ctx: StateContext<CompetencyBankStateModel>) {
    return this.competencyService.getAllCompetency().pipe(
      tap((returnData) => {
        const state = ctx.getState();

        ctx.setState({
          ...state,
          competencyBank: returnData,
        });
      })
    );
  }

  @Action(AddCompetencyBank)
  addDataToState(
    ctx: StateContext<CompetencyBankStateModel>,
    { payload }: AddCompetencyBank
  ) {
    return this.competencyService.addCompetency(payload).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Competency added successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();
        ctx.patchState({
          competencyBank: [...state.competencyBank, returnData],
        });
      })
    );
  }

  @Action(UpdateCompetencyBank)
  updateDataOfState(
    ctx: StateContext<CompetencyBankStateModel>,
    { payload, id }: UpdateCompetencyBank
  ) {
    return this.competencyService.updateCompetency(payload, id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Competency edited successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();

        const updatedCompetency = state.competencyBank.map((competencyBank) =>
          competencyBank.id === id ? returnData : competencyBank
        );

        ctx.patchState({
          competencyBank: updatedCompetency,
        });
      })
    );
  }

  @Action(DeleteCompetencyBank)
  deleteDataFromState(
    ctx: StateContext<CompetencyBankStateModel>,
    { id }: DeleteCompetencyBank
  ) {
    return this.competencyService.deleteCompetency(id).pipe(
      tap((returnData) => {
        this.alert.showToast(
          'Competency removed successfully',
          PrimeNgAlerts.SUCCESS
        );
        const state = ctx.getState();
        const filteredArray = state.competencyBank.filter(
          (contents: any) => contents.id !== id
        );

        ctx.setState({
          ...state,
          competencyBank: filteredArray,
        });
      })
    );
  }
}
