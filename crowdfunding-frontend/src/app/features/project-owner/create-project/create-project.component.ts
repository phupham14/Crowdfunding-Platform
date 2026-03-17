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

  constructor(private fb: FormBuilder, private projectService: ProjectService, private router: Router) {}

  ngOnInit(): void {
    this.projectForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
      funding_target: [0, Validators.required],
      category: ['', Validators.required],
      image: ['']
    });
  }

  onSubmit() {
    if (this.projectForm.invalid || this.isSubmitting) return;

    const payload = {
      name: this.projectForm.value.title,
      category: this.projectForm.value.category,
      funding_target: this.projectForm.value.funding_target,
      min_invest_amount: this.projectForm.value.min_invest_amount,
      status: 'OPEN'
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
