import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AdminDashboardService {

  private baseUrl = `${environment.apiUrl}/admin/dashboard/`;

  constructor(private http: HttpClient) {}

  getStats() {
    return this.http.get<any>(this.baseUrl);
  }
}