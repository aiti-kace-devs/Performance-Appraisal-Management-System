import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-staff-appraisal-section',
  templateUrl: './staff-appraisal-section.component.html',
  styleUrls: ['./staff-appraisal-section.component.scss'],
})
export class StaffAppraisalSectionComponent {
  @Input() formData: any;
}
