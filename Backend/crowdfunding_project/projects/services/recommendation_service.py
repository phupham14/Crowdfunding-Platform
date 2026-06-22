import numpy as np
import pandas as pd
from django.db.models import Count, Q, Sum

from interactions.models import UserInteraction
from projects.models import Project
from projects.services.recommendation_explanation_service import explain_recommendations
from projects.views.deepfm_recommendation import DeepFMRecommender
from risk_profiles.models import RiskProfile
from risk_profiles.services import get_allowed_project_risk_levels, get_risk_tier
from transactions.models import Transaction


N_CANDIDATES = 100
_deepfm_recommender = None


def get_deepfm_recommender():
    global _deepfm_recommender
    if _deepfm_recommender is None:
        _deepfm_recommender = DeepFMRecommender()
    return _deepfm_recommender


def to_float(value, default=0.0):
    if value is None:
        return default
    return float(value)


def risk_pref_from_tier(risk_tier):
    if risk_tier == "CONSERVATIVE":
        return 1.0
    if risk_tier == "BALANCED":
        return 2.0
    return 3.0


def duration_months(project):
    if not project.start_at or not project.end_at:
        return project.min_invest_duration_months or 0
    days = max((project.end_at - project.start_at).days, 0)
    return days / 30


def get_seen_project_ids(user):
    return set(
        Transaction.objects.filter(
            user=user,
            type="INVEST",
            status="SUCCESS",
            project_id__isnull=False,
        ).values_list("project_id", flat=True)
    )


def get_popularity_candidates(user, allowed_risk_levels, candidate_limit=N_CANDIDATES):
    seen_project_ids = get_seen_project_ids(user)
    limit = min(candidate_limit, N_CANDIDATES)

    candidates = list(
        Project.objects.filter(
            status="OPEN",
            risk_level__in=allowed_risk_levels,
        )
        .exclude(id__in=seen_project_ids)
        .annotate(
            invest_count=Count(
                "transaction",
                filter=(
                    Q(transaction__type="INVEST")
                    & Q(transaction__status="SUCCESS")
                ),
            ),
            invest_amount=Sum(
                "transaction__amount",
                filter=(
                    Q(transaction__type="INVEST")
                    & Q(transaction__status="SUCCESS")
                ),
            ),
        )
        .order_by("-invest_count", "-invest_amount", "-raised", "-created_at")[:limit]
    )

    if len(candidates) >= limit:
        return candidates

    fallback_seen_ids = seen_project_ids | {project.id for project in candidates}
    fallback_candidates = list(
        Project.objects.filter(
            status="OPEN",
            risk_level__in=allowed_risk_levels,
        )
        .exclude(id__in=fallback_seen_ids)
        .order_by("-raised", "-created_at")[: limit - len(candidates)]
    )
    return candidates + fallback_candidates


def get_user_history_features(user, risk_tier, candidates):
    candidate_categories = [project.category for project in candidates if project.category]
    user_tx = list(
        Transaction.objects.filter(
            user=user,
            type="INVEST",
            status="SUCCESS",
        ).select_related("project")
    )

    if not user_tx:
        candidate_aprs = [
            to_float(project.apr_expected)
            for project in candidates
            if project.apr_expected is not None
        ]
        return {
            "user_avg_apr": np.mean(candidate_aprs) if candidate_aprs else 0.0,
            "user_avg_risk": risk_pref_from_tier(risk_tier),
            "user_total_invest": 0.0,
            "user_top_category": candidate_categories[0] if candidate_categories else "",
            "top_risk_pref": risk_pref_from_tier(risk_tier),
        }

    user_aprs = [
        to_float(tx.project.apr_expected)
        for tx in user_tx
        if tx.project and tx.project.apr_expected is not None
    ]
    user_risks = [
        to_float(tx.project.risk_level)
        for tx in user_tx
        if tx.project and tx.project.risk_level is not None
    ]
    category_counts = {}
    risk_counts = {}

    for tx in user_tx:
        if not tx.project:
            continue
        category_counts[tx.project.category] = category_counts.get(tx.project.category, 0) + 1
        risk_counts[tx.project.risk_level] = risk_counts.get(tx.project.risk_level, 0) + 1

    return {
        "user_avg_apr": np.mean(user_aprs) if user_aprs else 0.0,
        "user_avg_risk": np.mean(user_risks) if user_risks else risk_pref_from_tier(risk_tier),
        "user_total_invest": sum(to_float(tx.amount) for tx in user_tx),
        "user_top_category": (
            max(category_counts, key=category_counts.get)
            if category_counts
            else (candidate_categories[0] if candidate_categories else "")
        ),
        "top_risk_pref": (
            max(risk_counts, key=risk_counts.get)
            if risk_counts
            else risk_pref_from_tier(risk_tier)
        ),
    }


def build_deepfm_frame(user, risk_profile, risk_tier, candidates):
    project_ids = [project.id for project in candidates]
    candidate_categories = [project.category for project in candidates if project.category]
    history = get_user_history_features(user, risk_tier, candidates)

    tx_qs = Transaction.objects.filter(type="INVEST", status="SUCCESS")
    investment_stats = {
        row["project_id"]: row
        for row in tx_qs.filter(project_id__in=project_ids)
        .values("project_id")
        .annotate(invest_count=Count("id"), invest_amount=Sum("amount"))
    }
    interaction_stats = {}
    for row in (
        UserInteraction.objects.filter(project_id__in=project_ids)
        .values("project_id", "interaction_type")
        .annotate(total=Count("id"))
    ):
        interaction_stats.setdefault(row["project_id"], {})[row["interaction_type"]] = row["total"]

    category_popularity = {
        row["project__category"]: row["total"]
        for row in tx_qs.filter(project__category__in=candidate_categories)
        .values("project__category")
        .annotate(total=Count("id"))
    }

    risk_pref = risk_pref_from_tier(risk_tier)
    top_risk_pref = int(min(max(round(float(history["top_risk_pref"])), 1), 3))
    age = to_float(risk_profile.age)
    income = to_float(risk_profile.income, 1.0)

    rows = []
    for project in candidates:
        invest = investment_stats.get(project.id, {})
        interactions = interaction_stats.get(project.id, {})
        invest_count = to_float(invest.get("invest_count"))
        invest_amount = to_float(invest.get("invest_amount"))
        view_count = to_float(interactions.get("view"))
        click_count = to_float(interactions.get("click"))

        funding_target = to_float(project.funding_target, 1.0)
        raised = to_float(project.raised)
        raised_ratio = raised / (funding_target + 1e-5)
        popularity = (
            invest_count * 3
            + invest_amount / 1_000_000
            + view_count * 0.2
            + click_count
            + raised_ratio * 2
        )
        apr_expected = to_float(project.apr_expected)
        risk_level = to_float(project.risk_level)

        rows.append({
            "project_id": project.id,
            "category": project.category or "",
            "top_risk_pref": str(top_risk_pref),
            "user_top_category": history["user_top_category"],
            "user_type": risk_tier,
            "age": age,
            "apr_diff": apr_expected - history["user_avg_apr"],
            "apr_expected": apr_expected,
            "apr_ratio": apr_expected / (history["user_avg_apr"] + 1e-5),
            "capacity": max(funding_target - raised, 0),
            "category_match": int((project.category or "") == history["user_top_category"]),
            "category_popularity": to_float(category_popularity.get(project.category)),
            "click": click_count,
            "duration": duration_months(project),
            "income": income,
            "item_popularity": invest_count + invest_amount / 1_000_000,
            "liquidity_score": to_float(project.liquidity_score),
            "log_apr": np.log1p(max(apr_expected, 0)),
            "log_income": np.log1p(max(income, 1)),
            "popularity": popularity,
            "return_per_risk": apr_expected / (risk_level + 1e-5),
            "risk_diff": abs(risk_level - history["user_avg_risk"]),
            "risk_gap": abs(risk_pref - risk_level),
            "risk_level": risk_level,
            "risk_match": int(round(risk_level) == top_risk_pref),
            "risk_pref": risk_pref,
            "risk_ratio": risk_level / (history["user_avg_risk"] + 1e-5),
            "user_avg_apr": history["user_avg_apr"],
            "user_avg_risk": history["user_avg_risk"],
            "user_total_invest": history["user_total_invest"],
            "view": view_count,
        })

    return pd.DataFrame(rows)


def get_recommendation_result(user, top_n=10, candidate_limit=100, include_explanations=True):
    risk_profile = RiskProfile.objects.filter(user=user).first()
    if not risk_profile:
        return {
            "error": "Please complete risk profiling first",
            "status_code": 400,
        }

    risk_tier = risk_profile.risk_tier or get_risk_tier(risk_profile.base_score or 0)
    allowed_risk_levels = get_allowed_project_risk_levels(risk_tier)
    candidates = get_popularity_candidates(
        user=user,
        allowed_risk_levels=allowed_risk_levels,
        candidate_limit=candidate_limit,
    )

    if not candidates:
        return {
            "risk_tier": risk_tier,
            "source": "none",
            "recommended_project_ids": [],
            "recommended_projects": [],
        }

    feature_frame = build_deepfm_frame(user, risk_profile, risk_tier, candidates)
    source = "deepfm"
    recommender = None
    try:
        recommender = get_deepfm_recommender()
        scored_frame = recommender.score_candidates({}, feature_frame)
        ranked_ids = scored_frame["project_id"].tolist()
    except Exception as exc:
        source = "popularity_fallback"
        scored_frame = feature_frame.sort_values(
            "popularity",
            ascending=False,
        )
        ranked_ids = scored_frame["project_id"].tolist()
        model_error = str(exc)[:500]
    else:
        model_error = None

    ranked_ids = ranked_ids[:top_n]
    project_by_id = {project.id: project for project in candidates}
    ranked_projects = [
        project_by_id[project_id]
        for project_id in ranked_ids
        if project_id in project_by_id
    ]
    explanations = {}
    if include_explanations:
        explanations = explain_recommendations(
            user=user,
            risk_tier=risk_tier,
            ranked_feature_frame=scored_frame,
            projects_by_id=project_by_id,
            source=source,
            recommender=recommender,
            top_n=top_n,
        )

    result = {
        "risk_tier": risk_tier,
        "source": source,
        "recommended_project_ids": ranked_ids,
        "recommended_projects": ranked_projects,
    }
    if include_explanations:
        result["explanations"] = explanations
    if model_error:
        result["model_error"] = model_error
    return result
