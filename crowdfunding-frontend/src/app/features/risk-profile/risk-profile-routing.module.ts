import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RiskProfileComponent } from './risk-profile/risk-profile.component';
import { InvestorGuard } from 'src/app/core/guards/investor/investor.guard';

const routes: Routes = [
  {
    path: '',
    component: RiskProfileComponent,
    canActivate: [InvestorGuard]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RiskProfileRoutingModule { }
