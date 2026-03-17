import { Component, OnInit } from '@angular/core';
import { ChartData, ChartOptions } from 'chart.js';
import { ReportService } from 'src/app/core/services/report.service';

@Component({
  selector: 'app-revenue-report',
  templateUrl: './revenue-report.component.html',
  styleUrls: ['./revenue-report.component.scss']
})
export class RevenueReportComponent implements OnInit {

  // Summary
  totalInvested: number = 0;        // thêm biến này
  estimatedProfit = 120000000;
  profitRate = 18.5;

  // Doughnut chart (profit rate)
  profitRateData!: ChartData<'doughnut'>;
  profitRateOptions: ChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  // Bar chart (estimated profit)
  profitBarData!: ChartData<'bar'>;

  // Line chart (profit over time)
  profitLineData!: ChartData<'line'>;          // thêm khai báo
  profitLineOptions: ChartOptions = {          // thêm khai báo
    responsive: true,
    plugins: { legend: { position: 'bottom' } },
    scales: { y: { beginAtZero: true } }
  };

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.loadRevenueReport();
  }

  private loadRevenueReport(): void {
    this.reportService.getRevenueReport().subscribe({
      next: (res: any) => {
        this.estimatedProfit = res.estimated_profit;
        this.profitRate = res.profit_rate;

        this.initCharts();
      },
      error: (err) => {
        console.error('Load revenue report failed', err);
      }
    });
  }

  private initCharts(): void {
    this.profitRateData = {
      labels: ['Profit', 'Remaining'],
      datasets: [
        {
          data: [
            this.profitRate,
            Math.max(0, 100 - this.profitRate)
          ]
        }
      ]
    };

    this.profitBarData = {
      labels: ['Estimated Profit'],
      datasets: [
        {
          label: 'VNĐ',
          data: [this.estimatedProfit]
        }
      ]
    };
  }
}
