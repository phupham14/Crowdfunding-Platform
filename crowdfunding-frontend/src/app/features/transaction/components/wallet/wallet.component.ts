import { Component, OnInit } from '@angular/core';
import { Wallet } from 'src/app/core/models/wallet.model';
import { TransactionService } from 'src/app/core/services/transaction.service';
import { firstValueFrom } from 'rxjs';
import {
  loadStripe,
  Stripe,
  StripeElements,
  StripeCardElement,
} from '@stripe/stripe-js';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.scss'],
})
export class WalletComponent implements OnInit {
  wallet!: Wallet;

  errorMessage = '';
  successMessage = '';
  isProcessing = false;

  amountFundIn = 0;

  stripe!: Stripe | null;
  elements!: StripeElements;
  card!: StripeCardElement;

  constructor(private transactionService: TransactionService) {}

  async ngOnInit() {
    // 🔥 PHẢI load Stripe trước
    this.stripe = await loadStripe(
      'pk_test_51TOKD0A6SZXlcVLm55VvRcOZHso9BmuwB3Ayp4ZKFK0rIh4Pbn48GomuyOG3UmBT9ECAUeAApJZW2mGg7bRtVdcN00OKhDa2ET',
    );

    if (!this.stripe) {
      this.errorMessage = 'Stripe failed to load';
      return;
    }

    this.elements = this.stripe.elements();

    this.card = this.elements.create('card', {
      style: {
        base: {
          fontSize: '16px',
        },
      },
    });

    this.card.mount('#card-element');

    this.card.on('change', (event) => {
      const displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError!.textContent = event.error.message;
      } else {
        displayError!.textContent = '';
      }
    });

    this.loadWallet();
  }

  loadWallet() {
    this.transactionService
      .getBalance()
      .subscribe((wallet) => (this.wallet = wallet));
  }

  async fundIn() {
    this.errorMessage = '';
    this.successMessage = '';

    if (this.amountFundIn <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      return;
    }

    // ✅ bắt đầu processing
    this.isProcessing = true;

    try {
      const res = await firstValueFrom(
        this.transactionService.fundIn({
          amount: this.amountFundIn,
          type: 'FUND_IN',
        }),
      );

      console.log('FUND IN RESPONSE:', res);

      const clientSecret = res.clientSecret;

      const { error, paymentIntent } = await this.stripe!.confirmCardPayment(
        clientSecret,
        {
          payment_method: {
            card: this.card,
          },
        },
      );

      console.log('paymentIntent:', paymentIntent);

      if (error) {
        console.error('Stripe error:', error);

        this.errorMessage = error.message || 'Payment failed';

        // ✅ mở lại button
        this.isProcessing = false;

        return;
      }

      if (paymentIntent?.status === 'succeeded') {
        this.successMessage = 'Payment submitted, waiting confirmation...';

        await firstValueFrom(
          this.transactionService.confirmPayment(paymentIntent.id)
        );

        this.loadWallet();
        this.successMessage = 'Fund in successful';
        this.isProcessing = false;
      }
    } catch (err: any) {
      console.error(err);

      this.errorMessage = err.error?.message || 'Fund in failed';

      // ✅ mở lại button
      this.isProcessing = false;
    }
  }

  onInvestSuccess() {
    this.loadWallet(); // refresh balance
  }
}
