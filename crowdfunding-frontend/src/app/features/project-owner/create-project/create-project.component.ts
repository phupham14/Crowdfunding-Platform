import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ProjectService } from 'src/app/core/services/project.service';

import { Router } from '@angular/router';

@Component({
  selector: 'app-create-project',
  templateUrl: './create-project.component.html',
  styleUrls: ['./create-project.component.scss']
})
export class CreateProjectComponent implements OnInit {
  projectForm!: FormGroup;
  isSubmitting = false;
  errorMessage = '';
  categories = [
    { id: 1, name: 'Technology' },
    { id: 2, name: 'Education' },
    { id: 3, name: 'Healthcare' },
    { id: 4, name: 'Finance' },
    { id: 5, name: 'Environment' },
    { id: 6, name: 'Arts' },
    { id: 7, name: 'Food' },
    { id: 8, name: 'Travel' },
    { id: 9, name: 'Sports' },
    { id: 10, name: 'Real Estate' },
    { id: 11, name: 'Fashion' },
    { id: 12, name: 'Music' },
    { id: 13, name: 'Film' },
    { id: 14, name: 'Publishing' },
    { id: 15, name: 'Gaming' },
    { id: 16, name: 'Cryptocurrency' },
    { id: 17, name: 'Agriculture' },
    { id: 18, name: 'Renewable Energy' },
    { id: 19, name: 'Construction' },
    { id: 20, name: 'Other' }
  ];

  constructor(private fb: FormBuilder, private projectService: ProjectService, private router: Router) {}

  ngOnInit(): void {
    this.projectForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      funding_target: [0, Validators.required],
      location: ['', Validators.required],
      start_date: ['', Validators.required],
      end_date: ['', Validators.required],
      category: ['', Validators.required],
      image: ['']
    });
  }

  formatDate(date: any): string {
    return date;
  }

  onSubmit() {
    if (this.projectForm.invalid || this.isSubmitting) return;

    const payload = {
      name: this.projectForm.value.title,
      category: this.projectForm.value.category,
      description: this.projectForm.value.description,
      funding_target: this.projectForm.value.funding_target,
      location: this.projectForm.value.location,
      start_at: this.formatDate(this.projectForm.value.start_date),
      end_at: this.formatDate(this.projectForm.value.end_date)
    };

    this.isSubmitting = true;
    this.errorMessage = '';

    this.projectService.createProject(payload).subscribe({
      next: () => {
        alert('Project created! Pending approval.');
        this.router.navigate(['/project-owner/my-projects']);
      },
      error: err => {
        this.errorMessage =
          err?.error?.message || 'Create project failed. Please try again.';
        this.isSubmitting = false;
      }
    });
  }

}
