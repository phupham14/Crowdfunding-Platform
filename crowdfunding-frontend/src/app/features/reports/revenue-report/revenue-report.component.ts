import { Component, OnInit } from '@angular/core';
import { ChartData, ChartOptions } from 'chart.js';
import { ReportService } from 'src/app/core/services/report.service';

interface RevenueTimelinePoint {
  label: string;
  invested?: number;
  profit?: number;
  revenue?: number;
}

@Component({
  selector: 'app-revenue-report',
  templateUrl: './revenue-report.component.html',
  styleUrls: ['./revenue-report.component.scss']
})
export class RevenueReportComponent implements OnInit {

  totalInvested = 0;
  estimatedProfit = 0;
  profitRate = 0;
  loading = false;
  error: string | null = null;

  profitRateData!: ChartData<'doughnut'>;
  valueComparisonData!: ChartData<'bar'>;
  revenueTrendData: ChartData<'line'> | null = null;

  profitRateOptions: ChartOptions<'doughnut'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom'
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.label}: ${context.parsed}%`
        }
      }
    },
    cutout: '62%'
  };

  valueComparisonOptions: ChartOptions<'bar'> = {
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
  };

  revenueTrendOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false
    },
    plugins: {
      legend: {
        position: 'bottom'
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.dataset.label}: ${this.formatCurrency(context.parsed.y ?? 0)}`
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
  };

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.loadRevenueReport();
  }

  private loadRevenueReport(): void {
    this.loading = true;
    this.error = null;

    this.reportService.getRevenueReport().subscribe({
      next: (res: any) => {
        this.totalInvested = this.toNumber(res.total_invested);
        this.estimatedProfit = this.toNumber(res.estimated_profit);
        this.profitRate = this.toNumber(res.profit_rate);

        this.initCharts(res);
        this.loading = false;
      },
      error: () => {
        this.error = 'Không thể tải báo cáo doanh thu';
        this.loading = false;
      }
    });
  }

  private initCharts(res: any): void {
    const safeProfitRate = Math.max(0, this.profitRate);
    const remainingRate = Math.max(0, 100 - safeProfitRate);

    this.profitRateData = {
      labels: ['Profit rate', 'Remaining to 100%'],
      datasets: [
        {
          data: [safeProfitRate, remainingRate],
          backgroundColor: ['#16a34a', '#e5e7eb'],
          borderColor: '#ffffff',
          borderWidth: 3
        }
      ]
    };

    const valueLabels = this.totalInvested > 0
      ? ['Total invested', 'Estimated profit']
      : ['Estimated profit'];
    const valueData = this.totalInvested > 0
      ? [this.totalInvested, this.estimatedProfit]
      : [this.estimatedProfit];

    this.valueComparisonData = {
      labels: valueLabels,
      datasets: [
        {
          label: 'VND',
          data: valueData,
          backgroundColor: this.totalInvested > 0 ? ['#2563eb', '#16a34a'] : ['#16a34a'],
          borderRadius: 8,
          maxBarThickness: 72
        }
      ]
    };

    this.revenueTrendData = this.buildTrendData(res.revenue_timeline || res.timeline || res.monthly_revenue);
  }

  private buildTrendData(points: RevenueTimelinePoint[] | undefined): ChartData<'line'> | null {
    if (!Array.isArray(points) || points.length === 0) {
      return null;
    }

    const labels = points.map((point) => point.label);
    const investedData = points.map((point) => this.toNumber(point.invested));
    const profitData = points.map((point) => this.toNumber(point.profit ?? point.revenue));

    return {
      labels,
      datasets: [
        {
          label: 'Invested',
          data: investedData,
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37, 99, 235, 0.12)',
          tension: 0.35,
          fill: false
        },
        {
          label: 'Profit',
          data: profitData,
          borderColor: '#16a34a',
          backgroundColor: 'rgba(22, 163, 74, 0.12)',
          tension: 0.35,
          fill: false
        }
      ]
    };
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
