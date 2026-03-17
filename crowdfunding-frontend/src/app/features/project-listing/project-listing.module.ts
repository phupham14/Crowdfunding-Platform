import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProjectListingComponent } from './project-listing.component';
import { ProjectListingRoutingModule } from './project-listing-routing.module';

@NgModule({
  declarations: [ProjectListingComponent],
  imports: [
    CommonModule,
    FormsModule,
    ProjectListingRoutingModule 
  ]
})
export class ProjectListingModule {}
