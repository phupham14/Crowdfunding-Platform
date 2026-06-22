import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProjectService } from 'src/app/core/services/project.service';
import { AuthService } from 'src/app/core/services/auth.service';

@Component({
  selector: 'app-project-detail',
  templateUrl: './project-detail.component.html',
  styleUrls: ['./project-detail.component.scss']
})
export class ProjectDetailComponent implements OnInit {
  project: any;
  showInvestModal = false;
  errorMessage = '';
  successMessage = '';
  recommendedProjects: any[] = [];
  isLoadingRecommendations = false;
  recommendationError = '';
  recommendationTitle = 'Dự án gợi ý';

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private projectService: ProjectService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe((params) => {
      const id = params.get('id');
      if (!id) return;

      this.loadProject(id);
    });

    this.loadRecommendations();
  }

  loadProject(id: string) {
    this.projectService.getProjectById(id).subscribe(data => {
      console.log(data);
      this.project = data;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  openInvestModal() {
    this.showInvestModal = true;
  }

  closeInvestModal() {
    this.showInvestModal = false;
  }

  onInvestSuccess() {
    this.showInvestModal = false;
    // reload project để cập nhật raised
    this.projectService.getProjectById(this.project.id)
      .subscribe(p => this.project = p);
  }

  getFundingProgress(): number {
    if (!this.project || !this.project.funding_target) return 0;
    return Math.min((this.project.raised / this.project.funding_target) * 100, 100);
  }

  loadRecommendations() {
    this.isLoadingRecommendations = true;
    this.recommendationError = '';

    const isLoggedIn = this.authService.isLoggedIn();
    const source$ = isLoggedIn
      ? this.projectService.getRecommendations()
      : this.projectService.getPopularProjects();

    this.recommendationTitle = isLoggedIn ? 'Dự án gợi ý' : 'Dự án phổ biến';

    source$.subscribe({
      next: (res: any) => {
        this.recommendedProjects = res.recommended_projects ?? [];
      },
      error: () => {
        this.recommendedProjects = [];
        this.recommendationError = 'Không thể tải gợi ý lúc này. Vui lòng thử lại sau.';
        this.isLoadingRecommendations = false;
      },
      complete: () => {
        this.isLoadingRecommendations = false;
      }
    });
  }

  goToProject(projectId: number) {
    this.router.navigate(['/project', projectId]);
  }
}
