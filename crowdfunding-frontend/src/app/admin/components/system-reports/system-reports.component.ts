import { Component, OnInit } from '@angular/core';
import { AdminSystemReportService } from 'src/app/core/services/admin/system-report.service';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-system-reports',
  templateUrl: './system-reports.component.html',
  styleUrls: ['./system-reports.component.scss']
})
export class SystemReportsComponent implements OnInit {

  report: any;
  loading = false;
  error: string | null = null;
  chart!: Chart;

  constructor(private reportService: AdminSystemReportService) {}

  ngOnInit(): void {
    this.loadReport();
  }

  loadReport() {
    this.loading = true;
    this.reportService.getSystemReport().subscribe({
      next: (res) => {
        this.report = res;
        this.loading = false;
        setTimeout(() => this.initChart(), 0); // đợi DOM render
      },
      error: () => {
        this.error = 'Không thể tải báo cáo hệ thống';
        this.loading = false;
      }
    });
  }

  initChart() {
    if (this.chart) {
      this.chart.destroy(); // tránh lỗi canvas reuse
    }

    this.chart = new Chart('systemReportChart', {
      type: 'bar',
      data: {
        labels: [
          'Users',
          'Projects',
          'Transactions',
          'Money Flow'
        ],
        datasets: [
          {
            label: 'System Overview',
            data: [
              this.report.total_users,
              this.report.total_projects,
              this.report.total_transactions,
              this.report.total_money_flow
            ],
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
}
