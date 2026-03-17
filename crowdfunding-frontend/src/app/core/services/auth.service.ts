import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
import { UserRole } from '../models/role.enum';

interface LoginResponse {
  access: string;   // access token
  refresh: string;  // refresh token
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private API = `${environment.apiUrl}/accounts`;

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.API}/login/`, { email, password });
  }

  register(payload: any) {
    return this.http.post(`${this.API}/register/`, payload);
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('role');
  }

  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  }

  isLoggedIn() {
    return !!this.getAccessToken();
  }

  getUserRole(): UserRole | null {
    const role = localStorage.getItem('role');
    return role ? role as UserRole : null;
  }

}
