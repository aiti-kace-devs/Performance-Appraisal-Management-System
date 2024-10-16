import { IAppraisalCycle } from '../../shared/interfaces';

//Read
export class GetAppraisalCycle {
  static readonly type = '[AppraisalCycle] Fetch';
}

//Create
export class AddAppraisalCycle {
  static readonly type = '[AppraisalCycle] Add';
  constructor(public payload: IAppraisalCycle) {}
}

//Update
export class UpdateAppraisalCycle {
  static readonly type = '[AppraisalCycle] Update';
  constructor(public payload: IAppraisalCycle, public id: string) {}
}

//Delete
export class DeleteAppraisalCycle {
  static readonly type = '[AppraisalCycle] Delete';
  constructor(public id: string) {}
}

export class SelectAppraisalCycle {
  static readonly type = '[AppraisalCycle] Fetch Details';
  constructor(public id: string) {}
}

export class ClearSelectedAppraisalCycle {
  static readonly type = '[AppraisalCycle] Clear';
}
