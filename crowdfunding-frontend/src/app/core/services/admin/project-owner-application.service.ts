import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AdminProjectOwnerApplicationService {
  private readonly baseUrl = `${environment.apiUrl}/accounts/project-owner-applications`;

  constructor(private http: HttpClient) {}

  getAllApplications(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/`);
  }

  approveApplication(id: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/${id}/approve/`, {});
  }

  rejectApplication(id: number, rejectReason: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/${id}/reject/`, {
      reject_reason: rejectReason
    });
  }
}
