import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './core/services/auth.service';
import { UserRole } from './core/models/role.enum';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  dropdownOpen = false;
  dashboardOpen: boolean = false;

  constructor(
    public authService: AuthService,
    private router: Router
  ) {}

  toggleDropdown() {
    this.dropdownOpen = !this.dropdownOpen;
    this.dashboardOpen = false;
  }

  goToDashboard() {
    const role = this.authService.getUserRole();

    switch (role) {
      case UserRole.INVESTOR:
        this.router.navigate(['/investor/dashboard']);
        break;
      case UserRole.PROJECT_OWNER:
        this.router.navigate(['/project-owner/my-projects']);
        break;
      case UserRole.ADMIN:
        this.router.navigate(['/admin/dashboard']);
        break;
      default:
        this.router.navigate(['/']);
    }

    this.dropdownOpen = false;
  }

  logout() {
    this.authService.logout();
    this.dropdownOpen = false;
    this.router.navigate(['/landing']);
  }
}
