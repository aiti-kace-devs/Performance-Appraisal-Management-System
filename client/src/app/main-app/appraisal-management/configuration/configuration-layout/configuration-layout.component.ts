import { Component, OnInit } from '@angular/core';
import { NavigationService } from '../../../../service/navigation.service';
import { MenuItem } from 'primeng/api';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IAppraisalCycle } from '../../../../shared/interfaces';
import { AppraisalCycleState } from '../../../../store/appraisal-cycle/appraisal-cycle.state';

@Component({
  selector: 'app-configuration-layout',
  templateUrl: './configuration-layout.component.html',
  styleUrls: ['./configuration-layout.component.scss'],
})
export class ConfigurationLayoutComponent implements OnInit {
  selectedCycle$: Observable<IAppraisalCycle | undefined> = this.store.select(
    AppraisalCycleState.getSelectedCycle
  );

  constructor(
    private store: Store,
    private route: ActivatedRoute,
    private readonly navigator: NavigationService
  ) {}

  ngOnInit() {
    this.route.params.subscribe((params) => {
      if (params && params['cycle_id']) {
        const cycleId = params['cycle_id'];
      }
    });

    this.selectedCycle$.subscribe((data) => {
      let cycle: any = {};
      cycle.name = data?.name;
      cycle.id = data?.id;
      this.setBreadCrumbs(cycle);
    });
  }

  setBreadCrumbs(cycle: any) {
    if (cycle) {
      const breadcrumbs: MenuItem[] = [];
      breadcrumbs.push(
        ...[
          {
            label: 'Appraisal',
          },
          {
            label: 'Appraisal Cycles',
            routerLink: '/admin/appraisal-management/configuration',
          },
          {
            label: cycle.name,
          },
        ]
      );
      this.navigator.breadCrumbs$.next(breadcrumbs);
    }
  }
}
