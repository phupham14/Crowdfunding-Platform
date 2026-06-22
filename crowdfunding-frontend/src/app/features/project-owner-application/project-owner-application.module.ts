import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { ApplyComponent } from './apply/apply.component';
import { ProjectOwnerApplicationRoutingModule } from './project-owner-application-routing.module';

@NgModule({
  declarations: [ApplyComponent],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ProjectOwnerApplicationRoutingModule
  ],
})
export class ProjectOwnerApplicationModule { }
