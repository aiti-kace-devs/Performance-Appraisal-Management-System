import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppAutoCompleteComponent } from './app-auto-complete.component';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [AppAutoCompleteComponent],
  imports: [CommonModule, AutoCompleteModule, FormsModule, ReactiveFormsModule],
  exports: [AppAutoCompleteComponent],
})
export class AppAutoCompleteModule {}
