import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';

import { SetStartLoading, SetStopLoading } from './app.action';

export class AppStateModel {
  loading = false;
}

@State<AppStateModel>({
  name: 'appState',
  defaults: {
    loading: false,
  },
})
@Injectable({
  providedIn: 'root',
})
export class AppState {
  @Selector()
  static getLoadingState(state: AppStateModel) {
    return state.loading;
  }

  @Action(SetStartLoading)
  startLoading(ctx: StateContext<AppStateModel>) {
    ctx.setState({
      loading: true,
    });
  }

  @Action(SetStopLoading)
  stopLoading(ctx: StateContext<AppStateModel>) {
    ctx.setState({
      loading: false,
    });
  }
}
