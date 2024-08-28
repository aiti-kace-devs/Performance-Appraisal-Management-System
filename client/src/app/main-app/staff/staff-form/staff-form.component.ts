import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-staff-form',
  templateUrl: './staff-form.component.html',
  styleUrl: './staff-form.component.scss',
})
export class StaffFormComponent implements OnInit {
  staffForm!: FormGroup;

  constructor(private formBuilder: FormBuilder) {}

  ngOnInit() {
    this.initializeForm();
  }

  initializeForm() {
    this.staffForm = this.formBuilder.group({
      title: ['', [Validators.required, Validators.minLength(2)]],
      first_name: ['', [Validators.required, Validators.minLength(3)]],
      last_name: ['', [Validators.required, Validators.minLength(3)]],
      other_name: ['', [Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      gender: ['', [Validators.required]],
      department: ['', [Validators.required]],
      position: ['', [Validators.required]],
      grade: ['', [Validators.required]],
      appointment_date: ['', [Validators.required]],
      role: [false],
    });
  }
}
