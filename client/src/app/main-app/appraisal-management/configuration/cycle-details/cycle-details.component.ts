import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CycleFormComponent } from '../cycle-form/cycle-form.component';

@Component({
  selector: 'app-cycle-details',
  templateUrl: './cycle-details.component.html',
  styleUrls: ['./cycle-details.component.scss'],
})
export class CycleDetailsComponent implements OnInit {
  @ViewChild('cycleForm')
  eventForm!: CycleFormComponent;
  cycleId!: any;
  showForm = false;
  data: any;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.route.params.subscribe((params) => {
      if (params && params['cycle_id']) {
        this.cycleId = params['cycle_id'];
        this.showForm = true;
      }
    });
  }
}
