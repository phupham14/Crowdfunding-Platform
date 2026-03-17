import { Component, OnInit } from '@angular/core';
import { ProjectService } from 'src/app/core/services/project.service';
import { UserService } from 'src/app/core/services/admin/user.service';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-user-management',
  templateUrl: './user-management.component.html',
  styleUrls: ['./user-management.component.scss']
})
export class UserManagementComponent implements OnInit {

  users: any[] = [];
  loading = false;
  error: string | null = null;

  // pagination
  currentPage = 1;
  pageSize = 10;
  totalItems = 0;
  ordering = 'id';

  // filters
  filterLocked = '';
  filterRole = '';

  selectedUser: any = null;

  constructor(
    private userService: UserService
  ) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(page: number = 1) {
    this.loading = true;
    this.currentPage = page;

    const params: any = {
      page: this.currentPage,
      page_size: this.pageSize,
    };

    if (this.filterLocked !== '') {
      params.locked = this.filterLocked;
    }

    if (this.filterRole) { 
      params.role = this.filterRole;
    }

    this.userService.getAllUsers(params)
      .pipe(finalize(() => this.loading = false))
      .subscribe({
        next: (res) => {
          this.ordering = params.ordering || this.ordering;
          this.users = res.results;
          this.totalItems = res.count;
        },
        error: () => {
          this.error = 'Không thể tải danh sách user';
        }
      });
  }

  toggleLock(user: any) {
    const action$ = user.locked
      ? this.userService.unblockUser(user.id)
      : this.userService.blockUser(user.id);

    action$.subscribe({
      next: () => {
        // cập nhật trạng thái trên UI
        user.locked = !user.locked;
      },
      error: () => alert('Thao tác thất bại')
    });
  }

  viewDetail(user: any) {
    this.userService.getUserById(user.id).subscribe({
      next: (res) => this.selectedUser = res,
      error: () => alert('Không thể tải user detail')
    });
  }

  closeDetail() {
    this.selectedUser = null;
  }

  onFilterChange() {
    this.loadUsers(1);
  }

  get totalPages(): number {
    return Math.ceil(this.totalItems / this.pageSize);
  }
}
