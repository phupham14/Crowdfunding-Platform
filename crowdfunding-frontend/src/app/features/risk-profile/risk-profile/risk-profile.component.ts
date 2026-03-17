import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RiskProfileService } from 'src/app/core/services/risk-profile.service';

@Component({
  selector: 'app-risk-profile',
  templateUrl: './risk-profile.component.html',
  styleUrls: ['./risk-profile.component.scss']
})
export class RiskProfileComponent implements OnInit {
  riskForm!: FormGroup;
  profile: any; // { base_score, risk_tier, ... }
  calculated = false;
  editing = true;

  constructor(private fb: FormBuilder, private riskService: RiskProfileService) {}

  ngOnInit(): void {
    this.riskForm = this.fb.group({
      age: [0, [Validators.required, Validators.min(0)]],
      annual_income_vnd_mil: [0, Validators.required],
      invest_experience_years: [0, Validators.required],

      risk_survey_raw: [0, Validators.required],
      volatility_tolerance_raw: [0, Validators.required],

      freq_trades_per_month: [0, Validators.required],
      max_drawdown_tol_pct: [0, Validators.required],
      diversification_level: [0, [Validators.required, Validators.min(0), Validators.max(1)]],

      has_leverage: [0, Validators.required],
      crypto_exposure_pct: [0, [Validators.required, Validators.min(0), Validators.max(100)]],

      horizon_years: [0, Validators.required],
      liquidity_need_level: [0, [Validators.required, Validators.min(0), Validators.max(1)]],
    });

    // Load profile cũ từ backend
    this.riskService.getMyRiskProfile().subscribe(data => {
      if (data) {
        this.profile = data;
        this.riskForm.patchValue(data);
        this.calculated = true;
        this.editing = false;
      }
    });
  }

  onCalculate() {
    const payload = this.riskForm.value;
    this.riskService.calculateRiskProfile(payload).subscribe(res => {
      this.profile = res;
      this.calculated = true;
      this.editing = true; // cho phép sửa lại
    });
  }

  onConfirm() {
    const payload = this.riskForm.value;
    this.riskService.confirmRiskProfile(payload).subscribe(() => {
      alert('Lưu hồ sơ rủi ro thành công!');
      this.editing = false;
    });
  }
}
