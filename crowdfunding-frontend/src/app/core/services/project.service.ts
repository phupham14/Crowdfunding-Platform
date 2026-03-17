import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Project } from '../models/project.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private readonly baseUrl = `${environment.apiUrl}/projects/`;

  constructor(private http: HttpClient) {}

  // Landing component sử dụng hàm này để lấy danh sách dự án
  getProjects(filters?: any): Observable<Project[]> {
    return this.http.get<Project[]>(this.baseUrl, { params: filters });
  }

  // Lấy danh sách dự án của user hiện tại (Project Owner)
  getMyProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.baseUrl}my-projects/`);
  }

  // Tạo dự án mới (Project Owner)
  createProject(payload: any): Observable<any> {
    return this.http.post(this.baseUrl, payload);
  }

  // Lấy thông tin chi tiết dự án theo ID (Project Owner)
  getProjectById(id: string): Observable<Project> {
    return this.http.get<Project>(`${this.baseUrl}${id}/`);
  }

  // Thay đổi trạng thái dự án (Project Owner)
  changeProjectStatus(id: string, status: string): Observable<any> {
    return this.http.post(`${this.baseUrl}${id}/change-status/`, { status });
  }

  // Cập nhật thông tin dự án (Project Owner)
  updateProject(id: string, payload: any): Observable<any> {
    return this.http.put(`${this.baseUrl}${id}/`, payload);
  }

  // Xoá dự án (Project Owner)
  deleteProject(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}${id}/`);
  }

  // core/services/project.service.ts
  // Lấy danh sách dự án được đề xuất cho người dùng
  getRecommendations() {
    return this.http.get<any[]>(
      `${this.baseUrl}recommendations/`
    );
  }

}
