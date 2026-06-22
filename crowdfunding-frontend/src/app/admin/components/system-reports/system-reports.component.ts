import { Component, OnDestroy, OnInit } from '@angular/core';
import { AdminSystemReportService } from 'src/app/core/services/admin/system-report.service';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-system-reports',
  templateUrl: './system-reports.component.html',
  styleUrls: ['./system-reports.component.scss']
})
export class SystemReportsComponent implements OnInit, OnDestroy {

  report: any;
  loading = false;
  error: string | null = null;
  private charts: Chart[] = [];

  constructor(private reportService: AdminSystemReportService) {}

  ngOnInit(): void {
    this.loadReport();
  }

  ngOnDestroy(): void {
    this.destroyCharts();
  }

  loadReport() {
    this.loading = true;
    this.reportService.getSystemReport().subscribe({
      next: (res) => {
        this.report = res;
        this.loading = false;
        setTimeout(() => this.initCharts(), 0);
      },
      error: () => {
        this.error = 'Không thể tải báo cáo hệ thống';
        this.loading = false;
      }
    });
  }

  initCharts() {
    this.destroyCharts();

    const userCount = this.toNumber(this.report.total_users);
    const projectCount = this.toNumber(this.report.total_projects);
    const transactionCount = this.toNumber(this.report.total_transactions);
    const moneyFlow = this.toNumber(this.report.total_money_flow);

    this.charts.push(new Chart('activityVolumeChart', {
      type: 'bar',
      data: {
        labels: ['Users', 'Projects', 'Transactions'],
        datasets: [
          {
            label: 'Total records',
            data: [userCount, projectCount, transactionCount],
            backgroundColor: ['#2563eb', '#16a34a', '#f59e0b'],
            borderRadius: 8,
            maxBarThickness: 52
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
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
    }));

    this.charts.push(new Chart('systemCompositionChart', {
      type: 'doughnut',
      data: {
        labels: ['Users', 'Projects', 'Transactions'],
        datasets: [
          {
            data: [userCount, projectCount, transactionCount],
            backgroundColor: ['#2563eb', '#16a34a', '#f59e0b'],
            borderColor: '#ffffff',
            borderWidth: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        },
        cutout: '62%'
      }
    }));

    this.charts.push(new Chart('moneyFlowChart', {
      type: 'bar',
      data: {
        labels: ['Money Flow'],
        datasets: [
          {
            label: 'Total money flow',
            data: [moneyFlow],
            backgroundColor: '#dc2626',
            borderRadius: 8,
            maxBarThickness: 72
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: (context) => this.formatCurrency(context.parsed.y ?? 0)
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: (value) => this.formatCompactCurrency(Number(value))
            }
          }
        }
      }
    }));
  }

  private destroyCharts(): void {
    this.charts.forEach((chart) => chart.destroy());
    this.charts = [];
  }

  private toNumber(value: unknown): number {
    return Number(value) || 0;
  }

  private formatCurrency(value: number): string {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
      maximumFractionDigits: 0
    }).format(value);
  }

  private formatCompactCurrency(value: number): string {
    return new Intl.NumberFormat('vi-VN', {
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);
  }
}
