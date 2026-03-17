import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard/dashboard.component';
import { InvestorRoutingModule } from './investor-routing.module';

@NgModule({
  declarations: [DashboardComponent],
  imports: [CommonModule, InvestorRoutingModule]
})
export class InvestorModule { }
