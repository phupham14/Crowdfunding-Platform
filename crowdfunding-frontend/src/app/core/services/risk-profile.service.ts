import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { RiskProfile, RiskTier } from '../models/risk-profile.model';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RiskProfileService {
  private readonly baseUrl = `${environment.apiUrl}/risk-profiles`;

  constructor(private http: HttpClient) {}

  getMyRiskProfile(): Observable<RiskProfile> {
    return this.http.get<RiskProfile>(`${this.baseUrl}/me/`);
  }

  calculateRiskProfile(payload: Partial<RiskProfile>): Observable<RiskProfile> {
    return this.http.post<RiskProfile>(`${this.baseUrl}/calculate/`, payload);
  }

  confirmRiskProfile(profile: Partial<RiskProfile>): Observable<RiskProfile> {
    return this.http.post<RiskProfile>(`${this.baseUrl}/confirm/`, profile);
  }
}