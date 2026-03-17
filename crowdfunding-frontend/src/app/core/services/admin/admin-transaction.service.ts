import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

@Injectable({ providedIn: 'root' })
export class AdminTransactionService {
  private readonly baseUrl = `${environment.apiUrl}/admin/transactions/`;

  constructor(private http: HttpClient) {}

  // Transaction history with admin-level filters
  getAdminTransactions(filters?: any): Observable<any> {
    return this.http.get<any>(this.baseUrl, { params: filters });
  }

}
