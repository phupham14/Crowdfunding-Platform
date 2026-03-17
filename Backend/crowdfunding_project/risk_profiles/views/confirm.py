from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from risk_profiles.ml.predictor import predict_base_score
from risk_profiles.services import get_risk_tier
from risk_profiles.models import RiskProfile
from accounts.permission import IsInvestor
from risk_profiles.domain.feature_engineering import compute_engineered_features

NUMERIC_FIELDS = [
    "age",
    "annual_income_vnd_mil",
    "invest_experience_years",
    "risk_survey_raw",
    "volatility_tolerance_raw",
    "freq_trades_per_month",
    "max_drawdown_tol_pct",
    "diversification_level",
    "has_leverage",
    "crypto_exposure_pct",
    "horizon_years",
    "liquidity_need_level"
]

class ConfirmRiskProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def post(self, request):
        raw_data = request.data

        # --- ép numeric toàn bộ input ---
        safe_data = {}
        for f in NUMERIC_FIELDS:
            val = raw_data.get(f, 0)
            try:
                safe_data[f] = float(val)
            except Exception:
                safe_data[f] = 0.0

        # --- feature engineering ---
        features = compute_engineered_features(safe_data)

        # --- predict base_score ---
        base_score = predict_base_score(features)

        # --- map risk tier ---
        risk_tier = get_risk_tier(base_score)

        # --- lưu xuống DB ---
        profile, _ = RiskProfile.objects.get_or_create(user=request.user)
        profile.raw_input = safe_data  # lưu numeric cleaned
        profile.base_score = base_score
        profile.risk_tier = risk_tier
        profile.model_version = "xgb_v1"
        profile.scored_at = timezone.now()
        profile.save()

        return Response({
            "user_id": request.user.id,
            "base_score": base_score,
            "risk_tier": risk_tier
        })
