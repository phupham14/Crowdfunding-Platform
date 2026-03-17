import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly baseUrl = `${environment.apiUrl}/admin/users/`;

  constructor(private http: HttpClient) {}

    getAllUsers(filters?: any): Observable<any> {
        return this.http.get<any>(this.baseUrl, { params: filters });
    }

    getUserById(id: string): Observable<any> {
        return this.http.get<any>(`${this.baseUrl}${id}/`);
    }

    blockUser(id: string): Observable<any> {
        return this.http.post(`${this.baseUrl}${id}/block/`, {});
    }

    unblockUser(id: string): Observable<any> {
        return this.http.post(`${this.baseUrl}${id}/unblock/`, {});
    }
  
}
