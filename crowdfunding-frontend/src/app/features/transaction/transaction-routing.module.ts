import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WalletComponent } from './components/wallet/wallet.component';
import { InvestmentComponent } from './components/investment/investment.component';

const routes: Routes = [
  { path: 'wallet', component: WalletComponent },
  { path: 'investment', component: InvestmentComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TransactionRoutingModule { }
