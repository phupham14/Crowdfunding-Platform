# risk_profiles/services.py

def get_risk_tier(base_score: int) -> str:
    if base_score <= 30:
        return "CONSERVATIVE"
    elif base_score <= 60:
        return "BALANCED"
    return "AGGRESSIVE"


def get_allowed_project_risk_levels(risk_tier: str):
    if risk_tier == "CONSERVATIVE":
        return [1, 2]
    elif risk_tier == "BALANCED":
        return [1, 2, 3]
    return [1, 2, 3, 4, 5]
