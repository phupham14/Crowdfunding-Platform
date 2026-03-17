import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({ providedIn: 'root' })
export class ReportService {
  private readonly baseUrl = `${environment.apiUrl}/reports`;

  constructor(private http: HttpClient) {}

  getPortfolioReport() {
    return this.http.get(`${this.baseUrl}/portfolio/`);
  }

  getRevenueReport() {
    return this.http.get(`${this.baseUrl}/revenue/`);
  }

}
