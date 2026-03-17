import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UserRole } from '../../models/role.enum';

@Injectable({
  providedIn: 'root'
})
export class InvestorGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): boolean | UrlTree {
    if (!this.authService.isLoggedIn()) {
      return this.router.createUrlTree(['/auth/login']);
    }

    const role = this.authService.getUserRole();

    if (role === UserRole.INVESTOR) {
      return true;
    }

    // Không phải investor → đá về 403 hoặc home
    return this.router.createUrlTree(['/']);
  }
}
