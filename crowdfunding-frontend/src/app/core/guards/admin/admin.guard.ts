import { Injectable } from '@angular/core';
import { CanActivate, CanActivateChild, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../../services/auth.service';
import { UserRole } from '../../models/role.enum';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate, CanActivateChild {

  constructor(private authService: AuthService, private router: Router) {}

  private checkAdmin(): boolean | UrlTree {
    const role = this.authService.getUserRole();
    if (role === UserRole.ADMIN) {
      return true;
    }
    // Nếu không phải admin, chuyển về login
    return this.router.createUrlTree(['/landing']);
  }

  canActivate(): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    return this.checkAdmin();
  }

  canActivateChild(): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    return this.checkAdmin();
  }
}
