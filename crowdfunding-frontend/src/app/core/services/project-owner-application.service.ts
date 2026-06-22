import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
import { ProjectOwnerApplication } from '../models/project-owner-application.model';

@Injectable({ providedIn: 'root' })
export class ProjectOwnerApplicationService {
  private readonly baseUrl = `${environment.apiUrl}/accounts/project-owner-applications`;

  constructor(private http: HttpClient) {}

  getMyApplication(): Observable<ProjectOwnerApplication> {
    return this.http.get<ProjectOwnerApplication>(`${this.baseUrl}/me/`);
  }

  submitApplication(payload: ProjectOwnerApplication): Observable<ProjectOwnerApplication> {
    return this.http.post<ProjectOwnerApplication>(`${this.baseUrl}/me/`, payload);
  }
}
