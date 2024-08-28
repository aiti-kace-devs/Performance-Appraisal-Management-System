import { IStaff } from '../../shared/interfaces';

//Read
export class GetStaff {
  static readonly type = '[Staff] Fetch';
}

//Create
export class AddStaff {
  static readonly type = '[Staff] Add';
  constructor(public payload: IStaff) {}
}

//Update
export class UpdateStaff {
  static readonly type = '[Staff] Update';
  constructor(public payload: IStaff, public id: string) {}
}

//Delete
export class DeleteStaff {
  static readonly type = '[Staff] Delete';
  constructor(public id: string) {}
}
