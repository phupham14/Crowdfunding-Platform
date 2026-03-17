import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UserRole } from '../../models/role.enum';

@Injectable({
  providedIn: 'root',
})
export class ProjectOwnerGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): boolean {
    if (!this.authService.isLoggedIn()) {
        this.router.navigate(['/login']);
        return false;
    }

    const role = this.authService.getUserRole();
    if (role === UserRole.PROJECT_OWNER) {
        return true;
    }

    this.router.navigate(['/']);
    return false;
  }

}
