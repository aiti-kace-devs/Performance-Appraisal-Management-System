import { Component } from '@angular/core';

@Component({
  selector: 'app-layout',
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.scss',
})
export class MainLayoutComponent {
  hideOnOutsideClick: boolean = true;
}
