import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AdminRoutingModule } from './admin-routing.module';
import { AdminDashboardComponent } from './components/dashboard/dashboard.component';
import { UserManagementComponent } from './components/user-management/user-management.component';
import { ProjectModerationComponent } from './components/project-moderation/project-moderation.component';
import { TransactionMonitoringComponent } from './components/transaction-monitoring/transaction-monitoring.component';
import { SystemReportsComponent } from './components/system-reports/system-reports.component';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    AdminDashboardComponent,
    UserManagementComponent,
    ProjectModerationComponent,
    TransactionMonitoringComponent,
    SystemReportsComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    AdminRoutingModule
  ]
})
export class AdminModule { }
