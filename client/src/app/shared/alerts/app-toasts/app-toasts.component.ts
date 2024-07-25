import { Component } from '@angular/core';

export enum ToastTypes {
  General = 'general',
  Error = 'error',
  Unobstrusive = 'unobstrusive',
}

@Component({
  selector: 'app-toasts',
  templateUrl: './app-toasts.component.html',
  styleUrls: ['./app-toasts.component.scss'],
})
export class AppToastsComponent {
  ToastTypes = ToastTypes;
}
