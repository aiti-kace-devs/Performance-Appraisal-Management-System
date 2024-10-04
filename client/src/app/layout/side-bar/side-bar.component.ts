import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss'],
})
export class SideBarComponent {
  // @Input()
  visible = false;

  closeCallback(): void {
    this.visible = !this.visible;
  }
}
