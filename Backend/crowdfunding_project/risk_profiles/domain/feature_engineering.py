def compute_engineered_features(user_input: dict) -> dict:
    age = user_input.get("age", 30)
    income = user_input.get("annual_income_vnd_mil", 0)
    experience = user_input.get("invest_experience_years", 0)

    risk_survey = user_input.get("risk_survey_raw", 50)
    volatility_tol = user_input.get("volatility_tolerance_raw", risk_survey)

    freq = user_input.get("freq_trades_per_month", 0)
    drawdown = user_input.get("max_drawdown_tol_pct", 0)
    diversification = user_input.get("diversification_level", 0.5)

    has_leverage = user_input.get("has_leverage", 0)
    crypto_pct = user_input.get("crypto_exposure_pct", 0)

    horizon = user_input.get("horizon_years", 1)
    liquidity = user_input.get("liquidity_need_level", 0.5)

    freq_norm = min(freq / 30, 1)
    dd_norm = min(drawdown / 50, 1)
    leverage_norm = has_leverage
    horizon_norm = min(horizon / 10, 1)
    liquidity_norm = liquidity

    behavior_score = (
        0.4 * freq_norm +
        0.4 * dd_norm +
        0.2 * (1 - diversification)
    )

    context_score = (
        0.6 * horizon_norm +
        0.4 * (1 - liquidity_norm)
    )

    survey_score = risk_survey / 100

    return {
        "age": age,
        "annual_income_vnd_mil": income,
        "invest_experience_years": experience,
        "risk_survey_raw": risk_survey,
        "volatility_tolerance_raw": volatility_tol,
        "freq_trades_per_month": freq,
        "max_drawdown_tol_pct": drawdown,
        "diversification_level": diversification,
        "has_leverage": has_leverage,
        "crypto_exposure_pct": crypto_pct,
        "horizon_years": horizon,
        "liquidity_need_level": liquidity,
        "freq_norm": freq_norm,
        "dd_norm": dd_norm,
        "leverage_norm": leverage_norm,
        "horizon_norm": horizon_norm,
        "liquidity_norm": liquidity_norm,
        "behavior_score": behavior_score,
        "context_score": context_score,
        "survey_score": survey_score,
    }
