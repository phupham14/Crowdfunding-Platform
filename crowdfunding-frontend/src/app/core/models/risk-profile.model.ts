import { User } from './user.model';

export type RiskTier = 'CONSERVATIVE' | 'BALANCED' | 'AGGRESSIVE';

export interface RiskProfile {
  id: number;
  user?: User;
  age?: number;
  income?: number;
  investment_experience?: number;
  risk_tolerance?: number;

  base_score: number; // DecimalField -> number
  risk_tier: RiskTier;

  updated_at?: string; // Date string ISO
  created_at?: string; // Date string ISO

  // Dữ liệu thô từ khảo sát
  risk_survey_raw?: number;
  freq_trades_per_month?: number;
  max_drawdown_tol_pct?: number;
  diversification_level?: number;
  horizon_years?: number;
  liquidity_need_level?: number;
}
