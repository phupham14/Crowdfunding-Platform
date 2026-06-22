import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Project } from 'src/app/core/models/project.model';
import { TransactionService } from 'src/app/core/services/transaction.service';
import { firstValueFrom } from 'rxjs';
import {
  loadStripe,
  Stripe,
  StripeElements,
  StripeCardElement,
} from '@stripe/stripe-js';

@Component({
  selector: 'app-investment',
  templateUrl: './investment.component.html',
  styleUrls: ['./investment.component.scss']
})
export class InvestmentComponent implements OnInit {
  @Input() project!: Project;
  @Output() close = new EventEmitter<void>();
  @Output() investSuccess = new EventEmitter<void>();

  amount = 0;
  errorMessage = '';
  successMessage = '';
  isProcessing = false;

  stripe!: Stripe | null;
  elements!: StripeElements;
  card!: StripeCardElement;

  constructor(private transactionService: TransactionService) {}

  async ngOnInit() {
    // 🔥 init Stripe
    this.stripe = await loadStripe('pk_test_51TOKD0A6SZXlcVLm55VvRcOZHso9BmuwB3Ayp4ZKFK0rIh4Pbn48GomuyOG3UmBT9ECAUeAApJZW2mGg7bRtVdcN00OKhDa2ET');

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

    // realtime error
    this.card.on('change', (event) => {
      const displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError!.textContent = event.error.message;
      } else {
        displayError!.textContent = '';
      }
    });
  }

  async confirmInvestment() {
    if (this.amount <= 0) {
      this.errorMessage = 'Amount must be greater than 0';
      return;
    }

    this.isProcessing = true;
    this.errorMessage = '';
    this.successMessage = '';

    try {
      // 1. gọi backend tạo payment intent
      const res = await firstValueFrom(
        this.transactionService.invest(this.project.id, this.amount)
      );

      const clientSecret = res.data.clientSecret;

      // 2. confirm payment với Stripe
      const { error, paymentIntent } =
        await this.stripe!.confirmCardPayment(clientSecret, {
          payment_method: {
            card: this.card,
          },
        });

      if (error) {
        this.errorMessage = error.message || 'Payment failed';
        this.isProcessing = false;
        return;
      }

      if (paymentIntent?.status === 'succeeded') {
        this.successMessage = 'Processing investment...';

        await firstValueFrom(
          this.transactionService.confirmPayment(paymentIntent.id)
        );

        this.successMessage = 'Investment successful';
        this.investSuccess.emit();
        this.close.emit();
        this.isProcessing = false;
      }

    } catch (err: any) {
      this.errorMessage = err.error?.message || 'Investment failed';
      this.isProcessing = false;
    }
  }
}