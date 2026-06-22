export interface Project {
  id: number;
  name: string;
  description: string;
  category: string;
  funding_target: number;
  raised: number;
  total_repaid: number;
  is_disbursed: boolean;

  expected_return?: number;
  liquidity_score?: number;
  risk_level?: 'LOW' | 'MEDIUM' | 'HIGH';
  min_invest_amount?: number;
  max_invest_amount?: number | null;
  start_at?: string;
  end_at?: string;
  investor_count?: number;

  start_date: string;
  end_date: string;

  summary?: string;
  explaination?: string;
  explanation?: {
    summary: string;
    top_factors?: any[];
    method?: string;
  };

  status:
    | 'PENDING'
    | 'REJECTED'
    | 'OPEN'
    | 'FUNDED'
    | 'REPAYING'
    | 'COMPLETED'
    | 'CANCELLED';

  created_at: string;
  updated_at: string;
}
