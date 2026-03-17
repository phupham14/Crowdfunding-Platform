import { Component, OnInit } from '@angular/core';
import { ChartData, ChartOptions } from 'chart.js';
import { ReportService } from 'src/app/core/services/report.service';

@Component({
  selector: 'app-portfolio-report',
  templateUrl: './portfolio-report.component.html',
  styleUrls: ['./portfolio-report.component.scss']
})
export class PortfolioReportComponent implements OnInit {

  totalInvested = 0;
  investmentCount = 0;
  investments: any[] = [];

  // Pie chart: project allocation
  allocationData!: ChartData<'pie'>;
  allocationOptions: ChartOptions = {
    responsive: true,
    plugins: { legend: { position: 'bottom' } }
  };

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.loadPortfolioReport();
  }

  private loadPortfolioReport(): void {
    this.reportService.getPortfolioReport().subscribe({
      next: (res: any) => {
        this.totalInvested = res.total_invested;
        this.investmentCount = res.investment_count;
        this.investments = res.investments;

        this.initCharts();
      },
      error: (err) => console.error('Load portfolio report failed', err)
    });
  }

  private initCharts(): void {
    // Nhóm theo project_id và tính tổng amount
    const allocationMap: Record<number, number> = {};
    this.investments.forEach(i => {
      if (!allocationMap[i.project_id]) allocationMap[i.project_id] = 0;
      allocationMap[i.project_id] += i.amount;
    });

    this.allocationData = {
      labels: Object.keys(allocationMap).map(id => `Project ${id}`),
      datasets: [
        { data: Object.values(allocationMap) }
      ]
    };
  }
}
