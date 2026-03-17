import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Project } from 'src/app/core/models/project.model';
import { TransactionService } from 'src/app/core/services/transaction.service';

@Component({
  selector: 'app-investment',  // Corrected selector to match HTML usage
  templateUrl: './investment.component.html',
  styleUrls: ['./investment.component.scss']
})
export class InvestmentComponent {
  @Input() project!: Project;
  @Output() close = new EventEmitter<void>();
  @Output() investSuccess = new EventEmitter<void>();  // Add this output

  amount = 0;
  errorMessage = '';
  successMessage = '';

  constructor(private transactionService: TransactionService) {}

  confirmInvestment() {
    if(this.amount <= 0) return;
    this.transactionService.invest(this.project.id, this.amount).subscribe({
      next: () => { 
        alert('Investment successful!'); 
        this.investSuccess.emit();  // Emit success event
        this.close.emit(); 
      },
      error: (err) => { alert('Error: ' + err.message); }
    });
  }
}