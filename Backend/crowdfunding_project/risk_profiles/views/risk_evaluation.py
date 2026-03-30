from datetime import datetime
from django.utils import timezone

# ======================
# EXPECTED RETURN (0–100)
# ======================
def calculate_expected_return_score(project):
    apr = project.apr_expected or 0

    if apr >= 0.3:
        return 100
    elif apr >= 0.2:
        return 80
    elif apr >= 0.1:
        return 60   
    elif apr >= 0.05:
        return 40
    else:
        return 20


# ======================
# LIQUIDITY (0–100)
# ======================
def calculate_liquidity_score(project):
    if project.funding_target == 0:
        return 0

    funding_ratio = project.raised / project.funding_target

    now = timezone.now()

    start = project.start_at
    end = project.end_at
    total_time = (end - start).total_seconds()
    elapsed_time = (now - start).total_seconds()

    time_progress = elapsed_time / total_time if total_time > 0 else 0

    score = 0

    # Funding progress (max 60)
    if funding_ratio > 0.7:
        score += 60
    elif funding_ratio > 0.4:
        score += 40
    else:
        score += 20

    # Early traction (max 40)
    if time_progress < 0.3 and funding_ratio > 0.4:
        score += 40
    elif time_progress < 0.5 and funding_ratio > 0.3:
        score += 20

    return min(score, 100)


# ======================
# RISK SCORE (1–5)
# ======================
def calculate_risk_score(project, expected_return_score, liquidity_score):
    score = 0

    funding_ratio = (
        project.raised / project.funding_target
        if project.funding_target > 0 else 0
    )

    # ===== Funding =====
    if funding_ratio < 0.2:
        score += 1
    elif funding_ratio < 0.5:
        score += 0.5

    # ===== APR =====
    if project.apr_expected is not None and project.apr_expected > 0.3:
        score += 1
    elif project.apr_expected is not None and project.apr_expected > 0.2:
        score += 0.7

    # ===== Duration =====
    if project.start_at is not None and project.end_at is not None:
        duration_days = (project.end_at - project.start_at).days
    else:
        duration_days = 0

    if duration_days > 180:
        score += 0.7
    elif duration_days > 90:
        score += 0.4

    # ===== Liquidity (normalize 0–1) =====
    liquidity = liquidity_score / 100
    score += (1 - liquidity)

    # ===== Return inconsistency =====
    expected_return = expected_return_score / 100
    if project.apr_expected is not None and project.apr_expected > 0.25 and expected_return < 0.5:
        score += 0.7

    # Normalize về 0–1
    score = min(score / 4, 1.0)

    # Map → 1–5
    return int(round(score * 4 + 1, 2))


# ======================
# MAP LEVEL
# ======================
def map_risk_level(score):
    if score <= 2:
        return 1  # Low
    elif score <= 4:
        return 3  # Medium
    else:
        return 5  # High


# ======================
# MAIN ENTRY
# ======================
def calculate_all_scores(project):
    expected_return = calculate_expected_return_score(project)
    liquidity = calculate_liquidity_score(project)

    risk = calculate_risk_score(
        project,
        expected_return_score=expected_return,
        liquidity_score=liquidity
    )

    risk_level = map_risk_level(risk)

    return {
        "expected_return_score": expected_return,
        "liquidity_score": liquidity,
        "risk_score": risk_level
    }