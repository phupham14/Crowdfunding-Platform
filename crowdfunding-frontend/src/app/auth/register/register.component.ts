import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/core/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  loading = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      full_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone: [''],
      password: ['', Validators.required]
    });
  }

  onRegister() {
    if (this.registerForm.invalid) return;

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const payload = this.registerForm.value;

    this.authService.register(payload).subscribe({
      next: (res: any) => {
        // lưu token nếu backend trả về
        if (res.access) {
          localStorage.setItem('access_token', res.access);
          localStorage.setItem('refresh_token', res.refresh);
        }

        // thông báo thành công
        this.successMessage = 'Đăng ký thành công';

        // delay để user nhìn thấy message
        setTimeout(() => {
          this.router.navigate(['/landing']);
        }, 1200);
      },
      error: (err) => {
        this.loading = false;

        // handle lỗi DRF trả về object
        if (err.error && typeof err.error === 'object') {
          this.errorMessage = Object.values(err.error).flat().join(', ');
        } else {
          this.errorMessage = 'Đăng ký thất bại';
        }
      },
      complete: () => {
        this.loading = false;
      }
    });
  }
}
