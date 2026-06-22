import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { FundInResponse } from '../models/fundin.model';
import { Wallet } from '../models/wallet.model';
import { environment } from 'src/environments/environment';

@Injectable({ providedIn: 'root' })
export class TransactionService {
  private readonly baseUrl = `${environment.apiUrl}/transactions/`;

  constructor(private http: HttpClient) {}

  getBalance(): Observable<Wallet> {
    return this.http.get<Wallet>(`${environment.apiUrl}/accounts/wallet/`);
  }

  fundIn(payload: { amount: number; description?: string; type: 'FUND_IN' }) {
    return this.http.post<FundInResponse>(`${this.baseUrl}fund-in/`, payload);
  }

  invest(projectId: number, amount: number): Observable<any> {
    return this.http.post(`${this.baseUrl}projects/${projectId}/invest/`, {
      amount,
      type: 'INVEST',
      description: 'Investment',
    });
  }

  disburseProject(projectId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}projects/${projectId}/disburse/`, {});
  }

  repayProject(projectId: number, amount: number): Observable<any> {
    return this.http.post(`${this.baseUrl}projects/${projectId}/repay/`, {
      amount,
    });
  }

  confirmPayment(paymentIntentId: string): Observable<any> {
    return this.http.post(`${this.baseUrl}confirm-payment/`, { paymentIntentId });
  }

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
