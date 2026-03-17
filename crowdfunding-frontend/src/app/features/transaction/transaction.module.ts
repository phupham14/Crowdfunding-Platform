import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TransactionRoutingModule } from './transaction-routing.module';
import { InvestmentComponent } from './components/investment/investment.component';
import { WalletComponent } from './components/wallet/wallet.component';
import { FormsModule } from '@angular/forms';


@NgModule({
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
