export class SelectSatffAppraisal {
  static readonly type = '[SatffAppraisal] Select';
  constructor(public id: string) {}
}

export class ClearSatffAppraisal {
  static readonly type = '[SatffAppraisal] Clear Selected';
}
