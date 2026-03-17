import { Component, OnInit } from '@angular/core';
import { ProjectService } from 'src/app/core/services/project.service';

@Component({
  selector: 'app-project-listing',
  templateUrl: './project-listing.component.html',
  styleUrls: ['./project-listing.component.scss']
})
export class ProjectListingComponent implements OnInit {
  projects: any[] = [];
  filters = { category: '', risk_level: '', funding_target: '' };

  constructor(private projectService: ProjectService) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.projectService.getProjects(this.filters).subscribe(data => {
      this.projects = data;
    });
  }

  onFilterChange(): void {
    this.loadProjects();
  }

  getRiskLabel(level: number): string {
    switch (level) {
      case 1: return 'Low';
      case 2: return 'Medium';
      case 3: return 'High';
      default: return 'Unknown';
    }
  }

  getRiskClass(level: number): string {
    switch (level) {
      case 1: return 'risk-low';
      case 2: return 'risk-medium';
      case 3: return 'risk-high';
      default: return '';
    }
  }

  getRaised(project: any): number {
    return +project.raised || 0;
  }

  getFundingTarget(project: any): number {
    return +project.funding_target || 1; // tránh chia 0
  }

  getProgressPercent(project: any): number {
    return (this.getRaised(project) / this.getFundingTarget(project)) * 100;
  }
}
