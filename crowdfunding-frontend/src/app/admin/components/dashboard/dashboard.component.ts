import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { AdminDashboardService } from 'src/app/core/services/admin/admin-dashboard.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class AdminDashboardComponent implements OnInit {

  totalUsers = 0;
  totalInvestment = 0;
  pendingProjects = 0;

  // filters
  filterLocked: string = '';
  filterRole: string = '';

  constructor(private dashboardService: AdminDashboardService) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard() {
    this.dashboardService.getStats().subscribe({
      next: (res) => {
        this.totalUsers = res.total_users;
        this.totalInvestment = res.total_investment;
        this.pendingProjects = res.pending_projects;
      }
    });
  }
}