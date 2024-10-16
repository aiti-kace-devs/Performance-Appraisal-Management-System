import {
  ChangeDetectorRef,
  Component,
  ComponentRef,
  signal,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { SelectAppraisalCycle } from '../../../../store/appraisal-cycle/appraisal-cycle.action';
import { debounceTime, finalize, map, Observable } from 'rxjs';
import { AppraisalCycleState } from '../../../../store/appraisal-cycle/appraisal-cycle.state';
import {
  IAppraisalCycle,
  IAppraisalSection,
} from '../../../../shared/interfaces';
import { OrderList } from 'primeng/orderlist';
import { SectionFormComponent } from '../section-form/section-form.component';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-cycle-details',
  templateUrl: './cycle-details.component.html',
  styleUrls: ['./cycle-details.component.scss'],
})
export class CycleDetailsComponent {
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
    private formBuilder: FormBuilder
  ) {}

  ngOnInit() {
    this.route.params.subscribe((params) => {
      if (params && params['cycle_id']) {
        this.cycleId = params['cycle_id'];
        this.store.dispatch(new SelectAppraisalCycle(this.cycleId));
      }
    });

    this.selectedCycle$.subscribe((data) => {
      this.sectionData = data?.appraisal_sections || [];
    });
  }

  deleteSection(i: number) {
    this.sectionData.splice(i, 1);
    this.selectFieldAndReturnComponent(null, -1);
  }

  addNewSections() {
    const newFieldGroup: FormGroup = this.formBuilder.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
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
}
