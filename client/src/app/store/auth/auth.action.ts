import { IUser } from '../../shared/interfaces';

//Read
export class GetLogggedInUser {
  static readonly type = '[Auth] Get User';
}

export class SetLogggedInUser {
  static readonly type = '[Auth] Set User';
  constructor(public user: IUser) {}
}

export class LogUserIn {
  static readonly type = '[Auth] Login User';
}

export class LogUserOut {
  static readonly type = '[Auth] Logout User';
}

export class GetUserAuthStatus {
  static readonly type = '[Auth] User Status';
}
