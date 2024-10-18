import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngxs/store';
import { AppAlertService } from '../../../../shared/alerts/service/app-alert.service';
import { IAppraisalCycle } from '../../../../shared/interfaces';
import {
  AddAppraisalCycle,
  UpdateAppraisalCycle,
} from '../../../../store/appraisal-cycle/appraisal-cycle.action';
import {
  catchError,
  filter,
  finalize,
  map,
  Observable,
  of,
  Subscription,
  take,
  tap,
} from 'rxjs';
import { PrimeNgAlerts } from '../../../../config/app-config';
import { AppraisalCycleState } from '../../../../store/appraisal-cycle/appraisal-cycle.state';

@Component({
  selector: 'app-cycle-form',
  templateUrl: './cycle-form.component.html',
  styleUrls: ['./cycle-form.component.scss'],
})
export class CycleFormComponent implements OnInit {
  @Input() data: IAppraisalCycle | undefined;

  @Output() cycleAdded = new EventEmitter();

  cycle$: Observable<IAppraisalCycle | undefined> = this.store.select(
    AppraisalCycleState.getSelectedCycle
  );

  cycleForm!: FormGroup;
  subscription$!: Subscription | undefined;

  constructor(
    private formBuilder: FormBuilder,
    private store: Store,
    private alert: AppAlertService,
    private cdref: ChangeDetectorRef // private config: DynamicDialogConfig // private dialogRef: DynamicDialogRef
  ) {}
  ngOnInit() {
    this.initializeForm();

    this.subscription$ = this.cycle$
      ?.pipe(filter((d) => !!d))
      .subscribe((cycle) => {
        this.data = cycle;
        if (this.data) {
          this.cycleForm.patchValue(this.data);
          this.cdref.detectChanges();
          this.cycleForm.updateValueAndValidity();
        }
      });
  }

  ngOnDestroy(): void {
    this.subscription$?.unsubscribe();
  }

  initializeForm() {
    this.cycleForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      description: ['', [Validators.required, Validators.minLength(3)]],
    });
  }

  submitForm() {
    if (this.cycleForm.valid) {
      let data = this.cycleForm.value;

      if (this.data?.id) {
        this.store.dispatch(new UpdateAppraisalCycle(data, this.data.id));
      } else {
        this.store
          .dispatch(new AddAppraisalCycle(data))
          .pipe(
            map((res: any) => {
              const cycle = res?.appraisalCycleState?.cycle as
                | IAppraisalCycle[]
                | undefined;

              const cle = cycle?.pop();
              if (cle?.id) {
                this.cycleAdded.next(cle.id);
              }
            }),
            take(1),
            catchError((error) => {
              this.alert.showToast(
                error.error.detail ||
                  'An error occurred while creating appraisal cycle.',
                PrimeNgAlerts.ERROR
              );
              return of(null);
            })
          )
          .subscribe();
      }
    }
  }
}
