from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.permission import IsInvestor
from risk_profiles.ml.predictor import predict_base_score
from risk_profiles.services import get_risk_tier
from risk_profiles.domain.feature_engineering import compute_engineered_features
from risk_profiles.serializers.serializers import RiskProfileSerializer

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

class CalculateRiskProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def post(self, request):
        raw_data = request.data

        # --- Ép numeric an toàn ---
        safe_data = {}
        for f in NUMERIC_FIELDS:
            val = raw_data.get(f, 0)
            try:
                safe_data[f] = float(val)
            except Exception:
                safe_data[f] = 0.0

        # --- Tính feature engineered ---
        features = compute_engineered_features(safe_data)

        # --- Predict base_score với XGBoost ---
        base_score = predict_base_score(features)  # đảm bảo features numeric hoàn toàn

        # --- Map sang risk tier ---
        risk_tier = get_risk_tier(base_score)

        return Response({
            "user_id": request.user.id,
            "base_score": base_score,
            "risk_tier": risk_tier
        })
