import { Component } from '@angular/core';
import { IColumnDef } from '../../../../shared/interfaces';

@Component({
  selector: 'app-key-area-list',
  templateUrl: './key-area-list.component.html',
  styleUrls: ['./key-area-list.component.scss'],
})
export class KeyAreaListComponent {
  columns: IColumnDef[] = [];
}
