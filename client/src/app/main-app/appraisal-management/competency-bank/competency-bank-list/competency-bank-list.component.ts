import { Component } from '@angular/core';
import { IColumnDef } from '../../../../shared/interfaces';

@Component({
  selector: 'app-competency-bank-list',
  templateUrl: './competency-bank-list.component.html',
  styleUrls: ['./competency-bank-list.component.scss'],
})
export class CompetencyBankListComponent {
  columns: IColumnDef[] = [];
}
