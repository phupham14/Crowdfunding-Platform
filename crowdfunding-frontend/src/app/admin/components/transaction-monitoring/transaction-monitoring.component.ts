import { Component, OnInit } from '@angular/core';
import { AdminTransactionService } from 'src/app/core/services/admin/admin-transaction.service';

@Component({
  selector: 'app-transaction-monitoring',
  templateUrl: './transaction-monitoring.component.html',
  styleUrls: ['./transaction-monitoring.component.scss']
})
export class TransactionMonitoringComponent implements OnInit {

  transactions: any[] = [];
  totalItems = 0;
  currentPage = 1;
  pageSize = 10;

  loading = false;
  error: string | null = null;

  filterStatus = '';
  filterType = '';

  constructor(private adminTransactionService: AdminTransactionService) {}

  ngOnInit(): void {
    this.loadTransactions();
  }

  loadTransactions(page: number = 1) {
    this.loading = true;
    this.currentPage = page;

    const params: any = {
      page: this.currentPage,
      page_size: this.pageSize,
      ordering: 'id'
    };

    if (this.filterStatus) params.status = this.filterStatus;
    if (this.filterType) params.type = this.filterType;

    this.adminTransactionService.getAdminTransactions(params).subscribe({
      next: (res) => {
        this.transactions = res.results;
        this.totalItems = res.count;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  onFilterChange() {
    this.currentPage = 1;
    this.loadTransactions(1);
  }

  get totalPages(): number {
    return Math.ceil(this.totalItems / this.pageSize);
  }
}
