import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProjectService } from 'src/app/core/services/project.service';
import { ChartData, ChartOptions } from 'chart.js';
import { Router } from '@angular/router';

@Component({
  selector: 'app-project-detail',
  templateUrl: './project-detail.component.html',
  styleUrls: ['./project-detail.component.scss']
})
export class ProjectDetailComponent implements OnInit {
  project: any;
  fundingChartData!: ChartData<'doughnut'>;
  fundingChartOptions: ChartOptions = { responsive: true };
  successMessage = '';
  errorMessage = '';

  constructor(private route: ActivatedRoute, private router: Router, private projectService: ProjectService) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.projectService.getProjectById(id).subscribe(data => {
      this.project = data;
      this.initChart();
    });
  }

  private initChart() {
    this.fundingChartData = {
      labels: ['Raised', 'Remaining'],
      datasets: [
        {
          data: [this.project.raised, this.project.funding_target - this.project.raised]
        }
      ]
    };
  }

  changeProjectStatus(status: string) {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.projectService.changeProjectStatus(id, status).subscribe({
      next: (res: any) => {
        // Cập nhật status local
        this.project.status = res.status; // lấy từ response backend
        this.initChart();

        // Hiển thị thông báo
        this.successMessage = `Cập nhật trạng thái thành công: ${res.status}`;
        setTimeout(() => (this.successMessage = ''), 3000); // 3s tự ẩn
      },
      error: (err) => {
        // Hiển thị lỗi từ backend nếu có
        this.errorMessage =
          err.error?.error || 'Không thể thay đổi trạng thái project';
        setTimeout(() => (this.errorMessage = ''), 5000); // tự ẩn sau 5s
      },
    });
  }

  goToEdit() {
    this.router.navigate(['/project-owner/edit', this.project.id]);
  }

  deleteProject() {
    if (!confirm('Bạn có chắc muốn xóa dự án này không?')) return;

    const id = this.project.id;

    this.projectService.deleteProject(id).subscribe({
      next: () => {
        alert('Xóa dự án thành công 🎉');
        // Chuyển về danh sách project sau khi xóa
        this.router.navigate(['/project-owner/my-projects']);
      },
      error: (err) => {
        alert(err.error?.detail || 'Xóa dự án thất bại');
      }
    });
  }

}
