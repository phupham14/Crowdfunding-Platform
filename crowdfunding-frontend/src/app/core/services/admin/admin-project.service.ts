import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Project } from '../../models/project.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ProjectService {
  private readonly baseUrl = `${environment.apiUrl}/admin/projects/`;

  constructor(private http: HttpClient) {}

  getAllProjects(filters?: any): Observable<Project[]> {
    return this.http.get<Project[]>(this.baseUrl, { params: filters });
  }

  getProjectById(id: string): Observable<Project> {
    return this.http.get<Project>(`${this.baseUrl}${id}/`);
  }

  approveProject(id: string): Observable<any> {
    return this.http.post(`${this.baseUrl}${id}/approve/`, {});
  }

  rejectProject(id: string, reason: string): Observable<any> {
    return this.http.post(`${this.baseUrl}${id}/reject/`, { reason });
  }
}
