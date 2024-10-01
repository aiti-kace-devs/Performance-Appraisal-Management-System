import { Component, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Select, Store } from '@ngxs/store';
import { StaffState } from '../../../store/staff/staff.state';
import { map, Observable } from 'rxjs';
import { IStaff } from '../../../shared/interfaces';
import { GetStaff } from '../../../store/staff/staff.action';

@Component({
  selector: 'app-staff-search',
  templateUrl: './staff-search.component.html',
  styleUrls: ['./staff-search.component.scss'],
})
export class StaffSearchComponent implements OnInit {
  @Input()
  formCtrl = new FormControl('');

  // @Select(StaffState.selectStateData) staff$!: Observable<IStaff[]>;
  staff$: Observable<IStaff[]> = this.store.select(StaffState.selectStateData);

  constructor(private store: Store) {}

  ngOnInit(): void {
    this.store.dispatch(new GetStaff());
  }

  staffSearchFunction(searchTerm: string) {
    this.staff$
      ?.pipe(
        map((staffMembers: IStaff[]) => {
          return staffMembers
            .filter((staff) =>
              staff.full_name?.toLowerCase().includes(searchTerm.toLowerCase())
            )
            .map((staff) => ({
              ...staff,
              label: staff.full_name,
            }));
        })
      )
      .subscribe();
  }
}

// map((staff: any[]) => {
//   const categoriesArray = [...categories];
//   return categoriesArray.map((cat) => {
//     return {
//       ...cat,
//       label: cat.name,
//     };
//   });
// })
