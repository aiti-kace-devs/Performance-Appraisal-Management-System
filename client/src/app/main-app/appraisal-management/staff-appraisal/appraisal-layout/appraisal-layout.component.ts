import { Component } from '@angular/core';
import { StaffAppraisalService } from '../service/staff-appraisal.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-appraisal-layout',
  templateUrl: './appraisal-layout.component.html',
  styleUrls: ['./appraisal-layout.component.scss'],
})
export class AppraisalLayoutComponent {
  staffId!: string;
  staffData: any;

  constructor(
    private appraisal: StaffAppraisalService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.route.params.subscribe((params) => {
      if (params && params['id']) {
        this.staffId = params['id'];
        this.appraisal.getStaffAppraisal(this.staffId).subscribe((data) => {
          this.staffData = data;
        });
      }
    });
  }
}
