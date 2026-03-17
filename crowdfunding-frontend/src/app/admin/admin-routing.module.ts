import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminDashboardComponent } from './components/dashboard/dashboard.component';
import { UserManagementComponent } from './components/user-management/user-management.component';
import { ProjectModerationComponent } from './components/project-moderation/project-moderation.component';
import { TransactionMonitoringComponent } from './components/transaction-monitoring/transaction-monitoring.component';
import { SystemReportsComponent } from './components/system-reports/system-reports.component';
import { AdminGuard } from 'src/app/core/guards/admin/admin.guard';

const routes: Routes = [
  {
    path: '',
    canActivate: [AdminGuard], 
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: AdminDashboardComponent },
      { path: 'users', component: UserManagementComponent },
      { path: 'projects', component: ProjectModerationComponent },
      { path: 'transactions', component: TransactionMonitoringComponent },
      { path: 'reports', component: SystemReportsComponent },
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule { }
