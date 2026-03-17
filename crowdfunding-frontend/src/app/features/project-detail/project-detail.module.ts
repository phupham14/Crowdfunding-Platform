import { NgModule } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { ProjectDetailComponent } from './project-detail.component';
import { ProjectDetailRoutingModule } from './project-detail-routing.module';
import { TransactionModule } from '../transaction/transaction.module';

@NgModule({
  declarations: [ProjectDetailComponent],
  imports: [
    CommonModule,
    ProjectDetailRoutingModule,
    TransactionModule
  ],
  providers: [CurrencyPipe]
})
export class ProjectDetailModule {}
