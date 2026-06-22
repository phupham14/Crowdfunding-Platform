import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ChartData, ChartOptions } from 'chart.js';

import { Project } from 'src/app/core/models/project.model';
import { ProjectService } from 'src/app/core/services/project.service';
import { TransactionService } from 'src/app/core/services/transaction.service';

@Component({
  selector: 'app-project-detail',
  templateUrl: './project-detail.component.html',
  styleUrls: ['./project-detail.component.scss']
})
export class ProjectDetailComponent implements OnInit {
  project!: Project;
  fundingChartData!: ChartData<'doughnut'>;
  fundingChartOptions: ChartOptions = { responsive: true };
  successMessage = '';
  errorMessage = '';
  repaymentAmount: number | null = null;
  isLoading = false;
  isDisbursing = false;
  isRepaying = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private projectService: ProjectService,
    private transactionService: TransactionService
  ) {}

  ngOnInit(): void {
    this.loadProject();
  }

  loadProject(): void {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.isLoading = true;

    this.projectService.getProjectById(id).subscribe({
      next: (data) => {
        this.project = data;
        this.initChart();
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Không thể tải thông tin dự án';
        this.isLoading = false;
      },
    });
  }

  private initChart(): void {
    const raised = this.project?.raised || 0;
    const target = this.project?.funding_target || 0;
    const remaining = Math.max(target - raised, 0);

    this.fundingChartData = {
      labels: ['Raised', 'Remaining'],
      datasets: [
        {
          data: [raised, remaining]
        }
      ]
    };
  }

  getRemainingRepayment(): number {
    return Math.max((this.project?.raised || 0) - (this.project?.total_repaid || 0), 0);
  }

  canDisburse(): boolean {
    return this.project?.status === 'FUNDED' && !this.project?.is_disbursed;
  }

  canRepay(): boolean {
    if (!this.project?.is_disbursed) {
      return false;
    }

    return this.project.status === 'FUNDED' || this.project.status === 'REPAYING';
  }

  changeProjectStatus(status: string): void {
    const id = this.route.snapshot.paramMap.get('id')!;

    this.projectService.changeProjectStatus(id, status).subscribe({
      next: (res: any) => {
        this.project.status = res.status;
        this.successMessage = `Cap nhat trang thai thanh cong: ${res.status}`;
        this.initChart();
        setTimeout(() => (this.successMessage = ''), 3000);
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Không thể thay đổi trạng thái dự án';
        setTimeout(() => (this.errorMessage = ''), 5000);
      },
    });
  }

  disburseProject(): void {
    if (!this.project || this.isDisbursing || !this.canDisburse()) {
      return;
    }

    this.isDisbursing = true;
    this.clearMessages();

    this.transactionService.disburseProject(this.project.id).subscribe({
      next: () => {
        this.successMessage = 'Giai ngan thanh cong';
        this.loadProject();
        this.isDisbursing = false;
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Không thể giải ngân cho dự án';
        this.isDisbursing = false;
      },
    });
  }

  repayProject(): void {
    if (!this.project || this.isRepaying || !this.repaymentAmount || this.repaymentAmount <= 0) {
      return;
    }

    this.isRepaying = true;
    this.clearMessages();

    this.transactionService.repayProject(this.project.id, this.repaymentAmount).subscribe({
      next: () => {
        this.successMessage = 'Hoan von thanh cong';
        this.repaymentAmount = null;
        this.loadProject();
        this.isRepaying = false;
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Không thể xử lý hoàn vốn cho dự án';
        this.isRepaying = false;
      },
    });
  }

  goToEdit(): void {
    this.router.navigate(['/project-owner/edit', this.project.id]);
  }

  deleteProject(): void {
    if (!confirm('Ban co chac muon xoa du an nay khong?')) {
      return;
    }

    const id = this.project.id;

    this.projectService.deleteProject(String(id)).subscribe({
      next: () => {
        alert('Xóa dự án thành công');
        this.router.navigate(['/project-owner/my-projects']);
      },
      error: (err) => {
        alert(err.error?.detail || 'Xóa dự án thất bại');
      }
    });
  }

  private clearMessages(): void {
    this.successMessage = '';
    this.errorMessage = '';
  }
}
