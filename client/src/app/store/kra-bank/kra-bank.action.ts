import { IKraBank } from '../../shared/interfaces';

//Read
export class GetKraBank {
  static readonly type = '[KraBank] Fetch';
}

//Create
export class AddKraBank {
  static readonly type = '[KraBank] Add';
  constructor(public payload: IKraBank) {}
}

//Update
export class UpdateKraBank {
  static readonly type = '[KraBank] Update';
  constructor(public payload: IKraBank, public id: string) {}
}

//Delete
export class DeleteKraBank {
  static readonly type = '[KraBank] Delete';
  constructor(public id: string) {}
}
