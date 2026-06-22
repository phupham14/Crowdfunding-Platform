import { Component, OnInit } from '@angular/core';
import { ProjectService } from 'src/app/core/services/project.service';

@Component({
  selector: 'app-project-listing',
  templateUrl: './project-listing.component.html',
  styleUrls: ['./project-listing.component.scss']
})
export class ProjectListingComponent implements OnInit {
  allProjects: any[] = [];
  filters = { category: '', risk_level: '', funding_target: '' };
  searchTerm = '';

  currentPage = 1;
  readonly pageSize = 9;

  constructor(private projectService: ProjectService) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.projectService.getProjects(this.filters).subscribe(data => {
      this.allProjects = data;
      this.currentPage = 1;
    });
  }

  onFilterChange(): void {
    this.loadProjects();
  }

  onSearch(): void {
    this.currentPage = 1;
  }

  get filteredProjects(): any[] {
    const term = this.searchTerm.trim().toLowerCase();
    if (!term) return this.allProjects;
    return this.allProjects.filter(p =>
      (p.name || '').toLowerCase().includes(term) ||
      (p.description || '').toLowerCase().includes(term)
    );
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.filteredProjects.length / this.pageSize));
  }

  get paginatedProjects(): any[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.filteredProjects.slice(start, start + this.pageSize);
  }

  get pageNumbers(): number[] {
    const total = this.totalPages;
    if (total <= 7) {
      return Array.from({ length: total }, (_, i) => i + 1);
    }
    const pages: number[] = [];
    if (this.currentPage <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i);
      pages.push(-1, total);
    } else if (this.currentPage >= total - 3) {
      pages.push(1, -1);
      for (let i = total - 4; i <= total; i++) pages.push(i);
    } else {
      pages.push(1, -1);
      for (let i = this.currentPage - 1; i <= this.currentPage + 1; i++) pages.push(i);
      pages.push(-1, total);
    }
    return pages;
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
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
    return +project.funding_target || 1;
  }

  getProgressPercent(project: any): number {
    return (this.getRaised(project) / this.getFundingTarget(project)) * 100;
  }
}
