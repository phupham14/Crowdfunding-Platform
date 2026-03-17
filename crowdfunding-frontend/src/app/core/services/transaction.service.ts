import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Transaction } from '../models/transaction.model';
import { map } from 'rxjs/operators';
import { Wallet } from '../models/wallet.model';
import { environment } from 'src/environments/environment';

@Injectable({ providedIn: 'root' })
export class TransactionService {
  private readonly baseUrl = `${environment.apiUrl}/transactions/`;

  constructor(private http: HttpClient) {}

  // Wallet
  getBalance(): Observable<Wallet> {
    return this.http.get<Wallet>(`${environment.apiUrl}/accounts/wallet/`);
  }

  // Fund In
  fundIn(payload: { amount: number; description?: string; type: 'FUND_IN' }) {
    return this.http.post(`${this.baseUrl}fund-in/`, payload);
  }

  // Withdraw
  withdraw(payload: {
    amount: number;
    description?: string;
    type: 'WITHDRAW';
  }) {
    return this.http.post(`${this.baseUrl}withdraw/`, payload);
  }

  // Invest
  invest(projectId: number, amount: number): Observable<any> {
    return this.http.post(`${this.baseUrl}projects/${projectId}/invest/`, {
      amount,
      type: 'INVEST', // bắt buộc match serializer choices
      description: 'Investment', // optional
    });
  }

  // Transaction history, filter theo type (INVEST / FUND_IN / WITHDRAW)
  getTransactions(): Observable<any[]> {
    return this.http.get<any>(`${this.baseUrl}history/?type=INVEST`).pipe(
      map((res) => {
        if (Array.isArray(res)) return res;
        if (res.results) return res.results;
        if (res.data) return res.data;
        return [];
      })
    );
  }
}
