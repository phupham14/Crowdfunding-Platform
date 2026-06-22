export interface ProjectOwnerApplication {
  id?: number;
  user_id?: number;
  user_email?: string;
  user_full_name?: string;
  business_name: string;
  business_type?: string;
  tax_code?: string;
  id_number?: string;
  bio?: string;
  experience?: string;
  document_url?: string;
  status?: 'PENDING' | 'APPROVED' | 'REJECTED';
  reject_reason?: string | null;
  reviewer_email?: string | null;
  reviewed_at?: string | null;
  created_at?: string;
  updated_at?: string;
}
