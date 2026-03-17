import { User } from './user.model';
import { UserRole } from './role.enum';

export interface LoginResponse {
  access: string;
  refresh: string;
  role: UserRole;
}
