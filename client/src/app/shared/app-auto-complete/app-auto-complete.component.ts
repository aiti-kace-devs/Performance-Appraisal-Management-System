import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  Input,
  Output,
  EventEmitter,
} from '@angular/core';
import { FormControl } from '@angular/forms';

const ENTER_KEY = 'Enter';

@Component({
  selector: 'app-auto-complete',
  templateUrl: './app-auto-complete.component.html',
  styleUrls: ['./app-auto-complete.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppAutoCompleteComponent implements OnInit {
  @Input() suggestions: any[] = [];

  @Input() control: FormControl = new FormControl();
  @Input() field = 'name';
  @Input() dataKey = 'id';
  @Input() dropdown = false;
  @Input() forceSelection = true;
  @Input() multiple = true;
  @Input() placeholder = '';

  @Output() searchEvent = new EventEmitter();
  @Output() enterKeyPressed = new EventEmitter();

  constructor() {}

  ngOnInit(): void {}

  search(event: any) {
    this.searchEvent.emit(event);
  }

  onKeyUp(event: any) {
    if (event instanceof KeyboardEvent) {
      const isEnterKey = event.key === ENTER_KEY;
      if (isEnterKey) {
        this.enterKeyPressed.emit();
      }
    }
  }
}
