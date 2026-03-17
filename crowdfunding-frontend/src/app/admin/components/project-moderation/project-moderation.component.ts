import { Component, OnInit } from '@angular/core';
import { Project } from 'src/app/core/models/project.model';
import { ProjectService } from 'src/app/core/services/admin/admin-project.service';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-project-moderation',
  templateUrl: './project-moderation.component.html',
  styleUrls: ['./project-moderation.component.scss'],
})
export class ProjectModerationComponent implements OnInit {
  projects: Project[] = [];
  public Math = Math; 
  loading = false;
  error: string | null = null;

  // Filter example: status / type
  filterStatus: string = '';
  filterType: string = '';

  currentPage = 1;
  pageSize = 10;
  totalItems = 0;

  constructor(private projectService: ProjectService) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(page: number = 1) {
    this.loading = true;
    this.currentPage = page;

    const filters: any = {
      page: this.currentPage,
      page_size: this.pageSize,
    };

    if (this.filterStatus) filters.status = this.filterStatus;
    if (this.filterType) filters.type = this.filterType;

    this.projectService
      .getAllProjects(filters)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: (res: any) => {
          this.projects = res.results;
          this.totalItems = res.count;
        },
        error: () => {
          this.error = 'Không thể tải danh sách project';
        },
      });
  }

  approveProject(id: string) {
    if (!confirm('Bạn có chắc muốn approve dự án này?')) return;

    this.projectService.approveProject(id).subscribe({
      next: () => {
        alert('Approve thành công!');
        this.loadProjects(); // reload
      },
      error: () => alert('Approve thất bại!'),
    });
  }

  rejectProject(id: string) {
    const reason = prompt('Nhập lý do reject:');
    if (!reason) return;

    this.projectService.rejectProject(id, reason).subscribe({
      next: () => {
        alert('Reject thành công!');
        this.loadProjects(); // reload
      },
      error: () => alert('Reject thất bại!'),
    });
  }

  // Filter change
  onFilterChange() {
    this.currentPage = 1;
    this.loadProjects(1);
  }
}
