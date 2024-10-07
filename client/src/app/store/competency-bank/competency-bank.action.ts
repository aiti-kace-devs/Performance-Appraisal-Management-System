import { ICompetencyBank } from '../../shared/interfaces';

//Read
export class GetCompetencyBank {
  static readonly type = '[CompetencyBank] Fetch';
}

//Create
export class AddCompetencyBank {
  static readonly type = '[CompetencyBank] Add';
  constructor(public payload: ICompetencyBank) {}
}

//Update
export class UpdateCompetencyBank {
  static readonly type = '[CompetencyBank] Update';
  constructor(public payload: ICompetencyBank, public id: string) {}
}

//Delete
export class DeleteCompetencyBank {
  static readonly type = '[CompetencyBank] Delete';
  constructor(public id: string) {}
}
