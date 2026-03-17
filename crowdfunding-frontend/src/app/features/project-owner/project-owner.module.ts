import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProjectOwnerRoutingModule } from './project-owner-routing.module';
import { MyProjectsComponent } from './my-projects/my-projects.component';
import { CreateProjectComponent } from './create-project/create-project.component';
import { ProjectDetailComponent } from './project-detail/project-detail.component';
import { ReactiveFormsModule } from '@angular/forms';
import { NgChartsModule } from 'ng2-charts';
import { ProjectEditComponent } from './project-edit/project-edit.component';


@NgModule({
  declarations: [
    MyProjectsComponent,
    CreateProjectComponent,
    ProjectDetailComponent,
    ProjectEditComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    NgChartsModule,
    ProjectOwnerRoutingModule
  ]
})
export class ProjectOwnerModule { }
