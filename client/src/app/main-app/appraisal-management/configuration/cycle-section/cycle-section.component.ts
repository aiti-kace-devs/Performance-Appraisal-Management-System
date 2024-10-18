import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  ComponentRef,
  OnInit,
  signal,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Store } from '@ngxs/store';
import {
  SelectAppraisalCycle,
  UpdateAppraisalCycleSection,
} from '../../../../store/appraisal-cycle/appraisal-cycle.action';
import { debounceTime, finalize, map, Observable } from 'rxjs';
import { AppraisalCycleState } from '../../../../store/appraisal-cycle/appraisal-cycle.state';
import {
  IAppraisalCycle,
  IAppraisalSection,
} from '../../../../shared/interfaces';
import { OrderList } from 'primeng/orderlist';
import { SectionFormComponent } from '../section-form/section-form.component';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AppAlertService } from '../../../../shared/alerts/service/app-alert.service';
import { PrimeNgAlerts } from '../../../../config/app-config';

@Component({
  selector: 'app-cycle-section',
  templateUrl: './cycle-section.component.html',
  styleUrls: ['./cycle-section.component.scss'],
})
export class CycleSectionComponent implements OnInit, AfterViewInit {
  @ViewChild('orderList') orderList!: OrderList;
  @ViewChild('formFieldContainer', { read: ViewContainerRef })
  formFieldContainer!: ViewContainerRef;

  selectedCycle$: Observable<IAppraisalCycle | null | undefined> =
    this.store.select(AppraisalCycleState.getSelectedCycle);

  disbledPicker$ = signal(false);
  sectionData: IAppraisalSection[] = [];

  selectedField$ = signal<null>(null);
  selectedIndex = -1;
  cycleId!: string;

  constructor(
    private route: ActivatedRoute,
    private store: Store,
    private cdref: ChangeDetectorRef,
    private formBuilder: FormBuilder,
    private alert: AppAlertService
  ) {}

  ngOnInit() {
    this.route.params.subscribe((params) => {
      if (params && params['cycle_id']) {
        this.cycleId = params['cycle_id'];
      }
    });

    this.selectedCycle$.subscribe((data) => {
      this.sectionData = data?.appraisal_sections || [];
      this.cdref.detectChanges();
    });
  }

  ngAfterViewInit(): void {
    this.cdref.detectChanges();
  }

  deleteSection(i: number) {
    this.sectionData.splice(i, 1);
    this.selectFieldAndReturnComponent(null, -1);
  }

  addNewSections() {
    const newFieldGroup: FormGroup = this.formBuilder.group({
      name: ['Appraisal', Validators.required],
      description: ['Description', Validators.required],
    });

    this.sectionData.push(newFieldGroup.value);

    this.selectFieldAndReturnComponent(
      newFieldGroup.value,
      this.sectionData.length - 1
    );
    this.cdref.detectChanges();
  }

  async selectFieldAndReturnComponent(data: any, index: number) {
    this.selectedField$.set(null);
    this.selectedField$.set(data);
    this.selectedIndex = index;
    this.orderList.selection = [data];
    this.orderList.cd.detectChanges();
    this.formFieldContainer.clear();
    let fieldComponent: ComponentRef<SectionFormComponent> | undefined =
      undefined;
    // create component and add to view

    if (data) {
      fieldComponent =
        this.formFieldContainer.createComponent(SectionFormComponent);
      fieldComponent.instance.data = data;
      // fieldComponent.instance.readonly = !isAdmin;
      const updateFormDataSubscription = fieldComponent.instance.onValueChange
        .pipe(
          debounceTime(500),
          map((_) => {
            const data = fieldComponent?.instance.sectionFormData;
            const fieldsData: any = [...this.sectionData];
            fieldsData[this.selectedIndex] = data;
            this.sectionData = fieldsData;

            fieldComponent?.hostView.detectChanges();
          }),
          finalize(() => this.cdref.detectChanges())
        )
        .subscribe();

      const statusChangeSubscription =
        fieldComponent.instance.onStatusChange.subscribe((status) => {
          if (status === 'INVALID') {
            this.disbledPicker$.set(true);
          }
          if (status === 'VALID') {
            this.disbledPicker$.set(false);
          }
          this.orderList.cd.detectChanges();
          this.cdref.detectChanges();
        });

      fieldComponent.onDestroy(() => {
        statusChangeSubscription.unsubscribe();
        updateFormDataSubscription.unsubscribe();
      });

      this.formFieldContainer.insert(fieldComponent.hostView);
    }
    return fieldComponent;
  }

  async submitSections() {
    if (this.sectionData.length === 0) {
      this.alert.showToast(
        'You cannot submit an empty form',
        PrimeNgAlerts.INFO
      );
      return;
    }

    // loop values and stop when an error is encountered
    for (const [index, inputData] of this.sectionData.entries()) {
      const fieldComponent = await this.selectFieldAndReturnComponent(
        inputData,
        index
      );

      const fieldIsInvalid = fieldComponent?.instance.isDataValid(inputData);

      if (!fieldIsInvalid) {
        this.alert.showToast(
          'Fix error on this field before proceeding',
          PrimeNgAlerts.ERROR
        );
        return;
      }
    }

    const formData = {
      appraisal_sections: this.sectionData,
      appraisal_cycle_id: this.cycleId,
    };

    this.store.dispatch(
      new UpdateAppraisalCycleSection(formData, this.cycleId)
    );
  }
}
