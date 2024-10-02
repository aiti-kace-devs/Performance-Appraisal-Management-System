import { IDepartment } from '../../shared/interfaces';

//Read
export class GetDepartment {
  static readonly type = '[Department] Fetch';
}

//Create
export class AddDepartment {
  static readonly type = '[Department] Add';
  constructor(public payload: IDepartment) {}
}

//Update
export class UpdateDepartment {
  static readonly type = '[Department] Update';
  constructor(public payload: IDepartment, public id: string) {}
}

//Delete
export class DeleteDepartment {
  static readonly type = '[Department] Delete';
  constructor(public id: string) {}
}

export class GetDepartmentMembers {
  static readonly type = '[Department] Fetch Members';
  constructor(public id: string) {}
}

export class ClearDepartmentMembers {
  static readonly type = '[Department] Clear Department Members';
}
