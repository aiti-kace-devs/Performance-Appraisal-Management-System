import {
  AfterViewInit,
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
export class SectionFormComponent implements AfterViewInit {
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

    this.sectionForm.valueChanges
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
    return data;
    // return {
    //   ...data,
    //   // validators: this.validatorForm.form.value,
    // };
  }

  get formIsInvalid() {
    return this.sectionForm.invalid;
  }

  isDataValid(data = this.data) {
    if (!data.name || !data.description) {
      return false;
    }

    return true;
  }
}
