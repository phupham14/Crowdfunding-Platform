import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ProjectOwnerApplicationService } from 'src/app/core/services/project-owner-application.service';

@Component({
  selector: 'app-project-owner-apply',
  templateUrl: './apply.component.html',
  styleUrls: ['./apply.component.scss']
})
export class ApplyComponent implements OnInit {
  loading = false;
  errorMessage = '';
  successMessage = '';
  currentStatus = '';

  form = this.fb.group({
    business_name: ['', Validators.required],
    business_type: [''],
    tax_code: [''],
    id_number: [''],
    bio: [''],
    experience: [''],
    document_url: [''],
  });

  constructor(
    private fb: FormBuilder,
    private applicationService: ProjectOwnerApplicationService
  ) {}

  ngOnInit(): void {
    this.loadMyApplication();
  }

  loadMyApplication() {
    this.applicationService.getMyApplication().subscribe({
      next: (res) => {
        this.currentStatus = res.status || '';
        this.form.patchValue(res);
      },
      error: () => {}
    });
  }

  submit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.applicationService.submitApplication(this.form.value as any).subscribe({
      next: (res) => {
        this.currentStatus = res.status || '';
        this.successMessage = 'Gui don thanh cong';
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = err.error?.detail || 'Gui don that bai';
        this.loading = false;
      }
    });
  }

  getStatusClass(): string {
    const status = (this.currentStatus || '').toLowerCase();
    return status || 'default';
  }
}
