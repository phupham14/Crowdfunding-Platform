import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PortfolioReportComponent } from './portfolio-report/portfolio-report.component';
import { RevenueReportComponent } from './revenue-report/revenue-report.component';
import { InvestorGuard } from 'src/app/core/guards/investor/investor.guard';

const routes: Routes = [
  {
    path: '',
    canActivate: [InvestorGuard],
    children: [
      { path: 'portfolio', component: PortfolioReportComponent },
      { path: 'revenue', component: RevenueReportComponent },
      { path: '', redirectTo: 'portfolio', pathMatch: 'full' }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ReportsRoutingModule {}
