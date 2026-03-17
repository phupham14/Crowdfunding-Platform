from rest_framework import serializers

class RiskProfileSerializer(serializers.Serializer):
    # Input từ FE
    age = serializers.IntegerField(default=30)
    annual_income_vnd_mil = serializers.IntegerField(default=0)
    invest_experience_years = serializers.IntegerField(default=0)

    risk_survey_raw = serializers.FloatField(default=50)
    volatility_tolerance_raw = serializers.FloatField(default=50)

    freq_trades_per_month = serializers.IntegerField(default=0)
    max_drawdown_tol_pct = serializers.FloatField(default=0)
    diversification_level = serializers.FloatField(default=0.5)
    has_leverage = serializers.IntegerField(default=0)
    crypto_exposure_pct = serializers.FloatField(default=0)

    horizon_years = serializers.IntegerField(default=1)
    liquidity_need_level = serializers.FloatField(default=0.5)

    # Output read-only
    base_score = serializers.FloatField(read_only=True)
    risk_tier = serializers.CharField(read_only=True)
