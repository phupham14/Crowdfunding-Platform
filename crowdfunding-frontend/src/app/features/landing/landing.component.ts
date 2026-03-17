import { Component, OnInit, Inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/core/services/auth.service';
import { UserRole } from 'src/app/core/models/role.enum';
import { Project } from 'src/app/core/models/project.model';
import { ProjectService } from 'src/app/core/services/project.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.scss']
})
export class LandingComponent implements OnInit {

  projects: any[] = [];   // ✅ KHAI BÁO BIẾN
  constructor(
    private authService: AuthService,
    private router: Router,
    private projectService: ProjectService
  ) { }

  ngOnInit(): void {
    // mock data 6 dự án
    this.projects = [
      {
        id: 1,
        title: 'Startup Nông nghiệp xanh',
        short_description: 'Ứng dụng công nghệ cao trong nông nghiệp',
        image: 'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=400&q=80',
        raised: 50000000,
        funding_target: 100000000
      },
      {
        id: 2,
        title: 'Ứng dụng giáo dục AI',
        short_description: 'Cá nhân hóa việc học bằng trí tuệ nhân tạo',
        image: 'https://cdn.prod.website-files.com/611e00fae5d1f200eb41e4e9/66b3be5a4f47d87bdc945227_image1-min-p-1600.png',
        raised: 80000000,
        funding_target: 120000000
      },
      {
        id: 3,
        title: 'Nền tảng sức khỏe số',
        short_description: 'Giám sát và chăm sóc sức khỏe từ xa',
        image: 'https://itbrief.asia/uploads/story/2024/12/11/techday_26169f03bf0a929134f3.webp',
        raised: 60000000,
        funding_target: 90000000
      },
      {
        id: 4,
        title: 'Ứng dụng fintech',
        short_description: 'Thanh toán & quản lý tài chính cá nhân',
        image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSebbC3FyA2ADpeYHDUe6AUFxPos6-YFYUhjA&s',
        raised: 45000000,
        funding_target: 80000000
      },
      {
        id: 5,
        title: 'Nông trại thông minh',
        short_description: 'IoT & AI tối ưu năng suất nông nghiệp',
        image: 'https://bna.1cdn.vn/thumbs/1200x630/2024/05/04/uploaded-annhanbna-2024_05_04-_anh-minh-hoa1-1883.jpg',
        raised: 70000000,
        funding_target: 120000000
      },
      {
        id: 6,
        title: 'Học trực tuyến đa ngôn ngữ',
        short_description: 'Nền tảng học tập toàn cầu cho học sinh',
        image: 'https://www.iworld.com.vn/wp-content/uploads/2021/08/2250x1500_czy-warto-korzystac-ze-szkolen-online-ollh.jpg',
        raised: 90000000,
        funding_target: 150000000
      }
    ];0
  }

  // joinAsProjectOwner() {
  //   if (!this.authService.isLoggedIn()) {
  //     // chưa đăng nhập → chuyển login
  //     this.router.navigate(['/auth/login']);
  //     return;
  //   }

  //   const role = this.authService.getUserRole();
  //   if (role !== UserRole.INVESTOR) {
  //     alert('Chỉ tài khoản Investor mới có thể tham gia làm chủ dự án.');
  //     return;
  //   }

  //   // Nếu là Investor → verify project owner
  //   this.projectService.verifyProjectOwner().subscribe({
  //     next: (res: any) => {
  //       if (res.is_project_owner) {
  //         // đã là project owner → chuyển thẳng sang dashboard project owner
  //         this.router.navigate(['/project-owner/my-projects']);
  //       } else {
  //         // chưa là project owner → mở form đăng ký
  //         this.router.navigate(['/project-owner/create']);
  //       }
  //     },
  //     error: (err) => {
  //       console.error(err);
  //       alert('Xảy ra lỗi, vui lòng thử lại.');
  //     }
  //   });
  // }
}
