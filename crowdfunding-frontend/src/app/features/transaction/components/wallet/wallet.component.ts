import { Component, OnInit } from '@angular/core';
import { Wallet } from 'src/app/core/models/wallet.model';
import { TransactionService } from 'src/app/core/services/transaction.service';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.scss'],
})
export class WalletComponent implements OnInit {
  wallet!: Wallet;

  errorMessage = '';
  successMessage = '';

  amountFundIn = 0;
  fundInDescription = '';

  amountWithdraw = 0;
  withdrawDescription = '';

  constructor(private transactionService: TransactionService) {}

  ngOnInit() {
    this.loadWallet();
  }

  loadWallet() {
    this.transactionService
      .getBalance()
      .subscribe((wallet) => (this.wallet = wallet));
  }

  fundIn() {
    this.errorMessage = '';
    this.successMessage = '';

    if (this.amountFundIn <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      return;
    }

    this.transactionService
      .fundIn({
        amount: this.amountFundIn,
        description: this.fundInDescription,
        type: 'FUND_IN',
      })
      .subscribe({
        next: () => {
          this.amountFundIn = 0;
          this.fundInDescription = '';
          setTimeout(() => { 
            this.successMessage = 'Fund in successful'; 
          }, 3000);
          console.log('Fund in successful');
          this.loadWallet();
        },
        error: (err) => {
          this.errorMessage = err.error?.message || 'Fund in failed';
        },
      });
  }

  withdraw() {
    this.errorMessage = '';
    this.successMessage = '';

    if (this.amountWithdraw <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      return;
    }

    this.transactionService
      .withdraw({
        amount: this.amountWithdraw,
        description: this.withdrawDescription,
        type: 'WITHDRAW',
      })
      .subscribe({
        next: () => {
          this.amountWithdraw = 0;
          this.withdrawDescription = '';
          setTimeout(() => { 
            this.successMessage = 'Withdraw successful'; 
          }, 3000);
          console.log('Withdraw successful');
          this.loadWallet();
        },
        error: (err) => {
          this.errorMessage = err.error?.message || 'Withdraw failed';
        },
      });
  }

  onInvestSuccess() {
    this.loadWallet(); // refresh balance
  }
}
