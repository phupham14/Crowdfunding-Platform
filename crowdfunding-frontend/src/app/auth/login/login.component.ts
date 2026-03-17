import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/core/services/auth.service';
import { UserRole } from 'src/app/core/models/role.enum';

export interface LoginResponse {
  access: string;
  refresh: string;
  role: UserRole; // role trả trực tiếp từ backend
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  onLogin() {
    debugger;
    if (this.loginForm.invalid) return;

    const { email, password } = this.loginForm.value;
    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.authService.login(email, password).subscribe({
      next: (res: any) => {
        // Lưu token
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('refresh_token', res.refresh);
        localStorage.setItem('role', res.role);

        console.log('Login response:', res);
        console.log('User role:', res.role);

        const role: UserRole = res.role;

        this.successMessage = 'Đăng nhập thành công 🎉';
        setTimeout(() => this.redirectByRole(role), 800);
      },
      error: (err) => {
        this.errorMessage = err.error?.detail || 'Email hoặc mật khẩu không đúng';
        this.loading = false;
      },
      complete: () => {
        this.loading = false;
      },
    });
  }

  private redirectByRole(role: UserRole) {
    debugger;
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
  }
}
