import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'appraisal-management';
  constructor(private router: Router) {}

  get adminRoute(): any {
    return this.router.url.includes('admin/');
  }
}
