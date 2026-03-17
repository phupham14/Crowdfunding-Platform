import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TransactionService } from 'src/app/core/services/transaction.service';
import { Transaction } from 'src/app/core/models/transaction.model';
import { ProjectService } from 'src/app/core/services/project.service';
import { Chart, ChartConfiguration, registerables } from 'chart.js';
import { RiskProfileService } from 'src/app/core/services/risk-profile.service';

Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  totalInvested = 0;
  atotalInvested = 0;
  activeProjects = 0;
  riskTier = '';
  estimatedROI = 0;
  baseScore = 0;

  investmentTimeline: any[] = [];
  activeInvestments: any[] = [];
  recommendedProjects: any[] = [];
  transactions: any[] = [];

  constructor(
    private router: Router,
    private transactionService: TransactionService,
    private projectService: ProjectService,
    private riskService: RiskProfileService
  ) {}

  ngOnInit(): void {
    this.renderChart();
    this.loadRecommendations();
    this.loadInvestments();
  }

  goToProject(projectId: number) {
    this.router.navigate(['/project', projectId]);
  }

  loadRecommendations() {
    this.projectService.getRecommendations().subscribe((res: any) => {
      console.log('RECOMMEND API:', res);

      // QUAN TRỌNG
      this.recommendedProjects = res.recommended_projects ?? [];
      this.riskTier = res.risk_tier;
      
    });
  }

  loadInvestments() {
    this.transactionService.getTransactions()
      .subscribe(tx => {
        this.computeDashboard(tx);
      });
  }

  calculateROI(transactions: Transaction[]): number {
    const totalFundIn = transactions
      .filter((t) => t.type === 'FUND_IN')
      .reduce((sum, t) => sum + t.amount, 0);

    const totalReturn = transactions
      .filter((t) => t.type === 'RETURN')
      .reduce((sum, t) => sum + t.amount, 0);

    if (totalFundIn === 0) return 0;

    return Number(
      (((totalReturn - totalFundIn) / totalFundIn) * 100).toFixed(2)
    );
  }

  computeDashboard(transactions: any[]) {
    /** 1. Tổng tiền đã đầu tư */
    this.totalInvested = transactions.reduce(
      (sum, t) => sum + Number(t.amount),
      0
    );

    /** 2. Dự án đang tham gia */
    const projectMap = new Map<number, any>();

    transactions.forEach((t) => {
      if (!projectMap.has(t.project)) {
        projectMap.set(t.project, {
          project_id: t.project,
          project_name: t.project_name,
          amount: 0,
          progress: t.project_progress ?? 0,
        });
      }
      projectMap.get(t.project).amount += Number(t.amount);
    });

    this.activeInvestments = Array.from(projectMap.values());
    this.activeProjects = this.activeInvestments.length;

    /** 3. Timeline đầu tư */
    const timeline = new Map<string, number>();
    transactions.forEach((t) => {
      const month = t.created_at.slice(0, 7); // yyyy-mm
      timeline.set(month, (timeline.get(month) || 0) + Number(t.amount));
    });

    this.investmentTimeline = Array.from(timeline.entries()).map(
      ([month, amount]) => ({ month, amount })
    );

    /** 4. Risk Tier */
    this.riskService.getMyRiskProfile().subscribe((profile) => {
      this.baseScore = profile.base_score;
      this.riskTier = profile.risk_tier;
    });

    /** 5. ROI ước tính (mock) */
    this.transactionService
      .getTransactions()
      .subscribe((transactions: Transaction[]) => {
        this.estimatedROI = this.calculateROI(transactions);
        this.renderChart();
      });
  }

  renderChart() {
    const ctx = document.getElementById('investmentChart') as HTMLCanvasElement;
    if (!ctx) return;

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: [
          'Tháng 1',
          'Tháng 2',
          'Tháng 3',
          'Tháng 4',
          'Tháng 5',
          'Tháng 6',
        ],
        datasets: [
          {
            label: 'Số tiền đầu tư',
            data: [
              20000000, 35000000, 50000000, 75000000, 100000000, 150000000,
            ],
            backgroundColor: 'rgba(34,197,94,0.2)',
            borderColor: 'rgba(34,197,94,1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value: number | string) {
                return new Intl.NumberFormat('vi-VN', {
                  style: 'currency',
                  currency: 'VND',
                }).format(Number(value));
              },
            },
          },
        },
      },
    } as ChartConfiguration);
  }
}
