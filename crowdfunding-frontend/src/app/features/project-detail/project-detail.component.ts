import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProjectService } from 'src/app/core/services/project.service';

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

  constructor(private route: ActivatedRoute, private projectService: ProjectService) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.projectService.getProjectById(id).subscribe(data => {
      console.log(data);
      this.project = data;
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
}

