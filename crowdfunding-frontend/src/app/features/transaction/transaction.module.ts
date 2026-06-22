import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TransactionRoutingModule } from './transaction-routing.module';
import { InvestmentComponent } from './components/investment/investment.component';
import { WalletComponent } from './components/wallet/wallet.component';
import { FormsModule } from '@angular/forms';
import { AdminGuard } from 'src/app/core/guards/admin/admin.guard';
import { InvestorGuard } from 'src/app/core/guards/investor/investor.guard';
import { ProjectOwnerGuard } from 'src/app/core/guards/project-owner/project-owner.guard';


@NgModule({
  // canActivate: [AdminGuard, InvestorGuard, ProjectOwnerGuard],
  declarations: [
    InvestmentComponent,
    WalletComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    TransactionRoutingModule
  ],
  exports: [WalletComponent, InvestmentComponent]
})
export class TransactionModule { }
