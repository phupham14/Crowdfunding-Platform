export interface Project {
  id: number;
  name: string;
  description: string;
  category: string;
  funding_target: number;
  raised: number;

  expected_return?: number;
  risk_level?: 'LOW' | 'MEDIUM' | 'HIGH';

  start_date: string;
  end_date: string;

  status: 'OPEN' | 'PENDING' | 'CLOSED' | 'REJECTED';

  created_at: string;
}
