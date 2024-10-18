import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { tap } from 'rxjs/operators';
import { IUser } from '../../shared/interfaces';
import { LoginService } from '../../auth/service/login.service';
import { GetUserAuthStatus, LogUserOut, SetLogggedInUser } from './auth.action';

export class AuthStateModel {
  loggedInUser: IUser | undefined | null;
}

@State<AuthStateModel>({
  name: 'authState',
  defaults: {
    loggedInUser: undefined,
  },
})
@Injectable({
  providedIn: 'root',
})
export class AuthState {
  constructor(private loginService: LoginService) {}

  @Selector()
  static getLoggedInUser(state: AuthStateModel) {
    return state.loggedInUser;
  }

  @Action(SetLogggedInUser)
  setLoggedInUser(
    ctx: StateContext<AuthStateModel>,
    { user }: SetLogggedInUser
  ) {
    const state = ctx.getState();

    ctx.setState({
      ...state,
      loggedInUser: user,
    });
  }

  @Action(LogUserOut)
  logUserOut(ctx: StateContext<AuthStateModel>) {
    const state = ctx.getState();

    ctx.setState({
      ...state,
      loggedInUser: undefined,
    });
  }

  @Action(GetUserAuthStatus)
  getUserAuthStatus(ctx: StateContext<AuthStateModel>) {
    // check locally if user exists otherwise check remotely
    return this.loginService.getMyDetails().pipe(
      tap((details) => {
        ctx.patchState({
          loggedInUser: details,
        });
      })
    );
  }
}
