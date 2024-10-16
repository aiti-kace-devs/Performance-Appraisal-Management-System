import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { IAppraisalSection } from '../../../../shared/interfaces';
import { debounceTime, distinctUntilChanged, merge } from 'rxjs';

@Component({
  selector: 'app-section-form',
  templateUrl: './section-form.component.html',
  styleUrls: ['./section-form.component.scss'],
})
export class SectionFormComponent {
  @Input() data: any = undefined;
  @Input() readonly = false;

  onValueChange = new EventEmitter();
  onStatusChange = new EventEmitter();

  public sectionForm!: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private cdref: ChangeDetectorRef
  ) {}

  ngAfterViewInit(): void {
    this.createSectionForm();

    if (this.data) {
      this.sectionForm.patchValue({
        ...this.data,
      });
    }

    merge(this.sectionForm.valueChanges)
      .pipe(
        debounceTime(200),
        distinctUntilChanged(
          (prev, curr) => JSON.stringify(curr) === JSON.stringify(prev)
        )
      )
      .subscribe((v) => this.onValueChange.next(this.sectionFormData));

    this.sectionForm.statusChanges
      .pipe(debounceTime(200), distinctUntilChanged())
      .subscribe((v) => this.onStatusChange.next(v));

    this.cdref.detectChanges;
  }

  async createSectionForm(readOnly = this.readonly) {
    this.sectionForm = this.formBuilder.group({
      name: [{ value: '', disabled: readOnly }, Validators.required],
      description: [{ value: '', disabled: readOnly }, Validators.required],
    });
  }

  get sectionFormData(): IAppraisalSection {
    const data = this.sectionForm.getRawValue();
    data.fieldType = data.fieldType?.value;
    return {
      ...data,
      // validators: this.validatorForm.form.value,
    };
  }
}
