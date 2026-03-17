import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ProjectService } from 'src/app/core/services/project.service';

@Component({
  selector: 'app-project-edit',
  templateUrl: './project-edit.component.html',
  styleUrls: ['./project-edit.component.scss'],
})
export class ProjectEditComponent implements OnInit {
  projectForm!: FormGroup;
  projectId!: string;
  loading = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private projectService: ProjectService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.projectId = this.route.snapshot.paramMap.get('id')!;
    this.initForm();
    this.loadProject();
  }

  initForm() {
    this.projectForm = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      category: ['', Validators.required],
      location: ['', Validators.required],
      funding_target: ['', [Validators.required, Validators.min(1)]],
      
      // thêm
      min_invest_amount: [0, Validators.required],
      max_invest_amount: [null],
      start_at: [null],
      end_at: [null],
    });
  }

  loadProject() {
    this.projectService.getProjectById(this.projectId).subscribe({
      next: (project) => {
        this.projectForm.patchValue(project);
      },
      error: () => {
        this.errorMessage = 'Không tải được thông tin project';
      },
    });
  }

  onSubmit() {
    if (this.projectForm.invalid) return;

    this.loading = true;
    this.successMessage = '';
    this.errorMessage = '';

    this.projectService
      .updateProject(this.projectId, this.projectForm.value)
      .subscribe({
        next: () => {
          this.successMessage = 'Cập nhật project thành công 🎉';
          setTimeout(() => {
            this.router.navigate(['/project-owner/my-projects']);
          }, 1200);
        },
        error: (err) => {
          this.errorMessage =
            err.error?.detail || 'Cập nhật project thất bại';
          this.loading = false;
        },
        complete: () => {
          this.loading = false;
        },
      });
  }
}
