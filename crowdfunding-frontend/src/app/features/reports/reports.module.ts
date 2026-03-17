import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgChartsModule } from 'ng2-charts';
import { ReportsRoutingModule } from './reports-routing.module';
import { PortfolioReportComponent } from './portfolio-report/portfolio-report.component';
import { RevenueReportComponent } from './revenue-report/revenue-report.component';


@NgModule({
  declarations: [
    PortfolioReportComponent,
    RevenueReportComponent,
  ],
  imports: [
    CommonModule,
    ReportsRoutingModule,
    NgChartsModule
  ]
})
export class ReportsModule { }
