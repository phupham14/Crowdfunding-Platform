import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AdminSystemReportService {
  private readonly baseUrl = `${environment.apiUrl}/admin/system-report/`;

  constructor(private http: HttpClient) {}

  getSystemReport(filters?: any): Observable<any> {
    return this.http.get<any>(this.baseUrl, { params: filters });
  }
  
}
