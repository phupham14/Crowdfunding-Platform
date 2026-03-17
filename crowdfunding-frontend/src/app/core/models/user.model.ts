import { UserRole } from '../models/role.enum.js';

export interface User {
  id: number;
  email: string;
  full_name: string;
  phone?: string;

  role: UserRole;

  bank_name?: string;
  bank_account?: string;
  bank_branch?: string;

  is_active: boolean;
  is_verified: boolean;

  created_at?: string; // ISO date string
  updated_at?: string; // ISO date string
}
