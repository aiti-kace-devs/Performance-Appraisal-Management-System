import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output,
  TemplateRef,
} from '@angular/core';
import { FormControl } from '@angular/forms';
import * as FileSaver from 'file-saver';
import { Observable, debounceTime, filter, of, switchMap, tap } from 'rxjs';
import { DEFAULT_PAGE_SIZE } from '../../config/app-config';

export enum ITableExportOptions {
  CSV = 'CSV',
  PDF = 'PDF',
  EXCEL = 'EXCEL',
}
@Component({
  selector: 'app-table',
  templateUrl: './app-table.component.html',
  styleUrls: ['./app-table.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppTableComponent implements OnInit {
  DEFAULT_PAGE_SIZE = DEFAULT_PAGE_SIZE;
  @Input()
  data: any[] = [];

  dataToDisplay!: any[];

  @Input()
  title!: string;

  @Input()
  batchAction = false;

  @Input()
  actionPositionLeft = false;

  @Input()
  batchActionTemplate: TemplateRef<any> | null = null;

  @Input()
  showAction = false;

  @Input()
  actionTemplate: TemplateRef<any> | null = null;

  @Input()
  bodyTemplate: TemplateRef<any> | null = null;

  @Input()
  headerTemplate: TemplateRef<any> | null = null;

  @Input()
  columnsDefinition!: {
    field: string;
    header: string;
    template?: TemplateRef<any>;
    subField?: string;
  }[];

  @Input()
  totalDataLength = 0;

  @Input()
  searchFunction: (toSearch: string) => Observable<any[]> = (query) => {
    const filtered = this.data?.filter((d) => {
      return (
        d.name?.toLowerCase().includes(query) ||
        d.full_name?.toLowerCase().includes(query) ||
        d.title?.toLowerCase().includes(query)
      );
    });

    return of(filtered || []);
  };

  @Input()
  searchPlaceholder = 'Enter value to search';

  @Input()
  showPaginator = true;

  @Input()
  refreshDataFunction: (() => any) | undefined = undefined;

  @Input()
  showCaption = true;

  @Input()
  getRowStyle = (rd: any) => {
    return {};
  };

  @Input() rowLink: boolean = false;
  @Input() rowLinkUrl: string = '';

  @Input() filename = 'download';

  @Input() showDownload = false;

  @Input() downloadOptions: ITableExportOptions[] = [
    ITableExportOptions.CSV,
    ITableExportOptions.PDF,
  ];

  @Output() pageChangeEvent = new EventEmitter();

  constructor(private cdref: ChangeDetectorRef) {}

  selectedData = [];
  searchFormControl = new FormControl('');

  tableExportOptions = ITableExportOptions;

  ngOnInit() {
    this.getPaginatedData();
    if (this.searchFunction) {
      this.dataToDisplay;
      this.searchFormControl.valueChanges
        .pipe(
          filter((value): value is string => value !== null),
          debounceTime(300),

          tap((_: string) => {
            if (_ === '') {
              this.getPaginatedData();
            }
          }),
          filter((d) => d.trim() !== ''),
          switchMap((search) => {
            return this.searchFunction(search.toLocaleLowerCase());
          })
        )
        .subscribe((d) => {
          this.dataToDisplay = [...d];
          this.cdref.detectChanges();
        });
    }
  }

  getPaginatedData() {
    if (this.data && this.columnsDefinition) {
      this.dataToDisplay = this.data.slice(0, DEFAULT_PAGE_SIZE);
    }

    if (!this.totalDataLength && this.data) {
      this.totalDataLength = this.data.length;
    }

    this.selectedData = [];
    this.cdref.detectChanges();
  }

  ngOnChanges(): void {
    this.getPaginatedData();
  }
  getOptions() {
    const options = [50, 100, 200];
    return options;
  }

  renderRow(rowData: any) {
    return this.getRowStyle(rowData);
  }

  onPageChange(event: any) {
    this.pageChangeEvent.emit(event);
  }

  refreshData() {
    if (this.refreshDataFunction) {
      this.refreshDataFunction();
    }
  }

  exportPdf() {
    const exportColumns = this.columnsDefinition.map((col) => ({
      title: col.header,
      dataKey: col.field,
    }));
    import('jspdf').then((jsPDF) => {
      import('jspdf-autotable').then((x) => {
        const doc = new jsPDF.default('l', 'px', 'a4');
        (doc as any).autoTable(exportColumns, this.data);
        doc.save(this.filename + Date.now() + '.pdf');
      });
    });
  }

  exportExcel() {
    import('xlsx').then((xlsx) => {
      const worksheet = xlsx.utils.json_to_sheet(this.data);
      const workbook = {
        Sheets: { data: worksheet },
        SheetNames: ['data'],
      };
      const excelBuffer: any = xlsx.write(workbook, {
        bookType: 'xlsx',
        type: 'array',
      });
      this.saveAsExcelFile(excelBuffer, this.filename);
    });
  }

  saveAsExcelFile(buffer: any, fileName: string): void {
    const EXCEL_TYPE =
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
    const EXCEL_EXTENSION = '.xlsx';
    const data: Blob = new Blob([buffer], {
      type: EXCEL_TYPE,
    });
    FileSaver.saveAs(
      data,
      fileName + '_export_' + new Date().getTime() + EXCEL_EXTENSION
    );
  }
}
