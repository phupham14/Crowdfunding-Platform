import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InvestorGuard } from 'src/app/core/guards/investor/investor.guard';

import { ApplyComponent } from './apply/apply.component';

const routes: Routes = [
  {
    path: '',
    canActivate: [InvestorGuard],
    children: [
      { path: '', component: ApplyComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ProjectOwnerApplicationRoutingModule {}
