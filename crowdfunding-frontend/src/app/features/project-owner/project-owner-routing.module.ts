import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MyProjectsComponent } from './my-projects/my-projects.component';
import { CreateProjectComponent } from './create-project/create-project.component';
import { ProjectDetailComponent } from './project-detail/project-detail.component';
import { ProjectEditComponent } from './project-edit/project-edit.component';
import { ProjectOwnerGuard } from 'src/app/core/guards/project-owner/project-owner.guard';

const routes: Routes = [
  {
    path: '',
    canActivate: [ProjectOwnerGuard],
    children: [
      { path: '', redirectTo: 'my-projects', pathMatch: 'full' },
      { path: 'my-projects', component: MyProjectsComponent },
      { path: 'create', component: CreateProjectComponent },
      { path: 'detail/:id', component: ProjectDetailComponent },
      { path: 'edit/:id', component: ProjectEditComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProjectOwnerRoutingModule { }
