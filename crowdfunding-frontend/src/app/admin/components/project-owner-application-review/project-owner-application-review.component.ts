import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs/operators';

import { AdminProjectOwnerApplicationService } from 'src/app/core/services/admin/project-owner-application.service';

@Component({
  selector: 'app-project-owner-application-review',
  templateUrl: './project-owner-application-review.component.html',
  styleUrls: ['./project-owner-application-review.component.scss']
})
export class ProjectOwnerApplicationReviewComponent implements OnInit {
  applications: any[] = [];
  filteredApplications: any[] = [];
  loading = false;
  errorMessage = '';
  successMessage = '';

  selectedStatus = '';
  selectedApplication: any = null;
  rejectReason = '';
  actionLoadingId: number | null = null;

  constructor(
    private applicationService: AdminProjectOwnerApplicationService
  ) {}

  ngOnInit(): void {
    this.loadApplications();
  }

  loadApplications() {
    this.loading = true;
    this.errorMessage = '';

    this.applicationService.getAllApplications()
      .pipe(finalize(() => this.loading = false))
      .subscribe({
        next: (res) => {
          this.applications = res || [];
          this.applyFilter();
        },
        error: () => {
          this.errorMessage = 'Khong the tai danh sach don dang ky';
        }
      });
  }

  applyFilter() {
    if (!this.selectedStatus) {
      this.filteredApplications = [...this.applications];
      return;
    }

    this.filteredApplications = this.applications.filter(
      (item) => item.status === this.selectedStatus
    );
  }

  openDetail(application: any) {
    this.selectedApplication = application;
    this.rejectReason = application.reject_reason || '';
    this.successMessage = '';
    this.errorMessage = '';
  }

  closeDetail() {
    this.selectedApplication = null;
    this.rejectReason = '';
  }

  approve(application: any) {
    this.successMessage = '';
    this.errorMessage = '';
    this.actionLoadingId = application.id;

    this.applicationService.approveApplication(application.id)
      .pipe(finalize(() => this.actionLoadingId = null))
      .subscribe({
        next: (updated) => {
          this.updateApplicationInList(updated);
          this.selectedApplication = updated;
          this.rejectReason = '';
          this.successMessage = 'Da approve don dang ky';
        },
        error: () => {
          this.errorMessage = 'Approve that bai';
        }
      });
  }

  reject(application: any) {
    if (!this.rejectReason.trim()) {
      this.errorMessage = 'Vui long nhap ly do reject';
      return;
    }

    this.successMessage = '';
    this.errorMessage = '';
    this.actionLoadingId = application.id;

    this.applicationService.rejectApplication(application.id, this.rejectReason.trim())
      .pipe(finalize(() => this.actionLoadingId = null))
      .subscribe({
        next: (updated) => {
          this.updateApplicationInList(updated);
          this.selectedApplication = updated;
          this.rejectReason = updated.reject_reason || '';
          this.successMessage = 'Da reject don dang ky';
        },
        error: () => {
          this.errorMessage = 'Reject that bai';
        }
      });
  }

  updateApplicationInList(updated: any) {
    this.applications = this.applications.map((item) =>
      item.id === updated.id ? updated : item
    );
    this.applyFilter();
  }

  getStatusClass(status: string): string {
    return (status || '').toLowerCase();
  }
}
