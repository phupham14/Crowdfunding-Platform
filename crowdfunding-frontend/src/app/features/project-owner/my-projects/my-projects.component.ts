import { Component, OnInit } from '@angular/core';
import { ProjectService } from 'src/app/core/services/project.service';
import { Router } from '@angular/router';
import { Project } from 'src/app/core/models/project.model';

@Component({
  selector: 'app-my-projects',
  templateUrl: './my-projects.component.html',
  styleUrls: ['./my-projects.component.scss']
})
export class MyProjectsComponent implements OnInit {
  projects: Project[] = [];

  constructor(private projectService: ProjectService, private router: Router) {}

  ngOnInit(): void {
    this.projectService.getMyProjects().subscribe(data => this.projects = data);
  }

  goToDetail(id: number) {
    this.router.navigate(['/project-owner/detail', id]);
  }

  getRemaining(project: Project): number {
    return (project.raised || 0) - (project.total_repaid || 0);
  }
}
