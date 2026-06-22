import json
import logging

import numpy as np
from django.conf import settings


logger = logging.getLogger(__name__)

SHAP_FEATURES = [
    "apr_expected",
    "risk_gap",
    "risk_diff",
    "category_match",
    "risk_match",
    "liquidity_score",
    "popularity",
    "return_per_risk",
    "capacity",
    "duration",
    "view",
    "click",
    "user_total_invest",
]

FACTOR_LABELS = {
    "apr_expected": "Lợi suất kỳ vọng",
    "apr_diff": "Chênh lệch lợi suất so với lịch sử",
    "category_match": "Phù hợp lĩnh vực quan tâm",
    "risk_match": "Trùng khẩu vị rủi ro",
    "risk_gap": "Khoảng cách rủi ro",
    "risk_diff": "Khác biệt so với rủi ro lịch sử",
    "liquidity_score": "Thanh khoản",
    "popularity": "Mức độ quan tâm",
    "item_popularity": "Lịch sử đầu tư vào dự án",
    "return_per_risk": "Lợi suất trên mỗi đơn vị rủi ro",
    "capacity": "Dư địa gọi vốn",
    "duration": "Thời hạn đầu tư",
    "view": "Lượt xem",
    "click": "Lượt nhấn",
    "score": "Điểm gợi ý",
}


def explain_recommendations(
    user,
    risk_tier,
    ranked_feature_frame,
    projects_by_id,
    source,
    recommender=None,
    top_n=6,
):
    explanations = {}
    if ranked_feature_frame is None or ranked_feature_frame.empty:
        return explanations

    top_frame = ranked_feature_frame.head(top_n).copy()
    shap_by_project = _build_shap_factors(recommender, ranked_feature_frame, top_frame)
    prepared_items = []

    for _, row in top_frame.iterrows():
        project_id = int(row["project_id"])
        project = projects_by_id.get(project_id)
        if not project:
            continue

        factors = shap_by_project.get(project_id) or _build_rule_factors(row, source)
        prepared_items.append({
            "project_id": project_id,
            "project": project,
            "row": row,
            "factors": factors,
            "method": "shap" if project_id in shap_by_project else "rules",
        })

    llm_summaries = _generate_llm_summaries(
        risk_tier=risk_tier,
        items=prepared_items,
        source=source,
    )

    for item in prepared_items:
        project_id = item["project_id"]
        project = item["project"]
        factors = item["factors"]
        summary = llm_summaries.get(project_id)
        if not summary:
            summary = _build_template_summary(project, risk_tier, factors, source)

        explanations[project_id] = {
            "summary": summary,
            "top_factors": factors,
            "method": item["method"],
        }

    return explanations


def _build_shap_factors(recommender, ranked_feature_frame, top_frame):
    if recommender is None:
        return {}

    enabled = getattr(settings, "RECOMMENDATION_EXPLANATIONS_USE_SHAP", False)
    if not enabled:
        return {}

    feature_names = [
        column
        for column in SHAP_FEATURES
        if column in ranked_feature_frame.columns
        and np.issubdtype(ranked_feature_frame[column].dtype, np.number)
    ]
    if not feature_names:
        return {}

    try:
        import shap
    except Exception as exc:
        logger.info("SHAP is not available for recommendation explanations: %s", exc)
        return {}

    explanations = {}
    x_background = (
        ranked_feature_frame.head(getattr(settings, "RECOMMENDATION_SHAP_BACKGROUND_SIZE", 20))[
            feature_names
        ]
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
        .to_numpy()
    )

    for _, row in top_frame.iterrows():
        project_id = int(row["project_id"])
        base_frame = row.to_frame().T
        x_explain = (
            base_frame[feature_names]
            .replace([np.inf, -np.inf], 0)
            .fillna(0)
            .to_numpy()
        )

        def predict_from_features(feature_matrix):
            import pandas as pd

            feature_matrix = np.asarray(feature_matrix)
            rows = []
            for values in feature_matrix:
                candidate = base_frame.copy()
                for index, feature in enumerate(feature_names):
                    candidate[feature] = values[index]
                rows.append(candidate)

            candidate_frame = pd.concat(rows, ignore_index=True)
            return recommender.predict_scores(candidate_frame)

        try:
            explainer = shap.KernelExplainer(predict_from_features, x_background)
            shap_values = explainer.shap_values(
                x_explain,
                nsamples=getattr(settings, "RECOMMENDATION_SHAP_NSAMPLES", 50),
            )
        except Exception as exc:
            logger.info("SHAP explanation failed for project %s: %s", project_id, exc)
            continue

        values = np.asarray(shap_values)
        if values.ndim > 2:
            values = values[0]
        values = values.reshape(1, -1)

        factors = []
        for feature_index, feature in enumerate(feature_names):
            impact_value = float(values[0][feature_index])
            if abs(impact_value) < 1e-8:
                continue
            factors.append(_factor_payload(feature, row.get(feature), impact_value))

        factors.sort(key=lambda item: abs(item["impact_value"]), reverse=True)
        if factors:
            explanations[project_id] = factors[:3]

    return explanations


def _build_rule_factors(row, source):
    factors = []

    if source == "popularity_fallback":
        factors.append(_factor_payload("popularity", row.get("popularity"), 1.0))
        if row.get("view", 0) > 0:
            factors.append(_factor_payload("view", row.get("view"), 0.5))
        if row.get("click", 0) > 0:
            factors.append(_factor_payload("click", row.get("click"), 0.5))
        return factors[:3]

    if row.get("category_match", 0) == 1:
        factors.append(_factor_payload("category_match", row.get("category"), 1.0))
    if row.get("risk_match", 0) == 1 or row.get("risk_gap", 999) <= 0.5:
        factors.append(_factor_payload("risk_gap", row.get("risk_gap"), 0.9))
    if row.get("apr_diff", 0) > 0:
        factors.append(_factor_payload("apr_diff", row.get("apr_diff"), 0.8))
    if row.get("liquidity_score", 0) >= 3:
        factors.append(_factor_payload("liquidity_score", row.get("liquidity_score"), 0.6))
    if row.get("popularity", 0) > 0:
        factors.append(_factor_payload("popularity", row.get("popularity"), 0.5))
    if row.get("return_per_risk", 0) > 0:
        factors.append(_factor_payload("return_per_risk", row.get("return_per_risk"), 0.4))

    return factors[:3] or [_factor_payload("score", row.get("score"), 0.1)]


def _factor_payload(feature, value, impact_value):
    return {
        "feature": feature,
        "label": FACTOR_LABELS.get(feature, feature),
        "value": _json_safe_value(value),
        "impact": "positive" if impact_value >= 0 else "negative",
        "impact_value": round(float(impact_value), 6),
    }


def _generate_llm_summary(project, risk_tier, factors, row, source):
    api_key = getattr(settings, "GOOGLE_API_KEY", None)
    if not api_key or not getattr(settings, "RECOMMENDATION_EXPLANATIONS_USE_LLM", True):
        return None

    try:
        from google import genai
    except Exception as exc:
        logger.info("Google GenAI SDK is not available: %s", exc)
        return None

    prompt = {
        "task": "Viết một câu giải thích ngắn bằng tiếng Việt cho gợi ý đầu tư.",
        "rules": [
            "Không cam kết lợi nhuận.",
            "Không đưa lời khuyên tài chính tuyệt đối.",
            "Chỉ dùng dữ liệu được cung cấp.",
            "Tối đa 2 câu.",
        ],
        "project": {
            "name": project.name,
            "category": project.category,
            "apr_expected": _json_safe_value(project.apr_expected),
            "risk_level": project.risk_level,
            "liquidity_score": project.liquidity_score,
        },
        "user": {
            "risk_tier": risk_tier,
        },
        "recommendation": {
            "source": source,
            "score": _json_safe_value(row.get("score")),
            "factors": factors,
        },
    }

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=getattr(settings, "GOOGLE_AI_MODEL", "gemini-2.5-flash"),
            contents=json.dumps(prompt, ensure_ascii=False),
        )
    except Exception as exc:
        logger.info("Gemini explanation failed: %s", exc)
        return None

    return (getattr(response, "text", "") or "").strip()[:500] or None


def _generate_llm_summaries(risk_tier, items, source):
    api_key = getattr(settings, "GOOGLE_API_KEY", None)
    if not api_key or not getattr(settings, "RECOMMENDATION_EXPLANATIONS_USE_LLM", True):
        return {}
    if not items:
        return {}

    try:
        from google import genai
    except Exception as exc:
        logger.info("Google GenAI SDK is not available: %s", exc)
        return {}

    prompt = {
        "task": "Viet cau giai thich ngan bang tieng Viet cho tung goi y dau tu.",
        "rules": [
            "Khong cam ket loi nhuan.",
            "Khong dua loi khuyen tai chinh tuyet doi.",
            "Chi dung du lieu duoc cung cap.",
            "Moi project toi da 2 cau.",
            "Chi tra ve JSON object hop le, khong markdown.",
        ],
        "user": {
            "risk_tier": risk_tier,
        },
        "response_format": {
            "summaries": {
                "project_id": "summary",
            },
        },
        "recommendations": [
            {
                "project_id": item["project_id"],
                "source": source,
                "score": _json_safe_value(item["row"].get("score")),
                "project": {
                    "name": item["project"].name,
                    "category": item["project"].category,
                    "apr_expected": _json_safe_value(item["project"].apr_expected),
                    "risk_level": item["project"].risk_level,
                    "liquidity_score": item["project"].liquidity_score,
                },
                "factors": item["factors"],
            }
            for item in items
        ],
    }

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=getattr(settings, "GOOGLE_AI_MODEL", "gemini-2.5-flash"),
            contents=json.dumps(prompt, ensure_ascii=False),
        )
    except Exception as exc:
        logger.info("Gemini explanation failed: %s", exc)
        return {}

    return _parse_llm_summaries(getattr(response, "text", "") or "")


def _parse_llm_summaries(response_text):
    response_text = response_text.strip()
    if not response_text:
        return {}
    if response_text.startswith("```"):
        response_text = response_text.strip("`").strip()
        if response_text.startswith("json"):
            response_text = response_text[4:].strip()

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as exc:
        logger.info("Gemini explanation response was not JSON: %s", exc)
        return {}

    summaries = data.get("summaries", data)
    if not isinstance(summaries, dict):
        return {}

    parsed = {}
    for project_id, summary in summaries.items():
        if not summary:
            continue
        try:
            parsed[int(project_id)] = str(summary).strip()[:500]
        except (TypeError, ValueError):
            continue
    return parsed


def _build_template_summary(project, risk_tier, factors, source):
    labels = [factor["label"].lower() for factor in factors[:3]]
    if source == "popularity_fallback":
        reason = ", ".join(labels) if labels else "độ phổ biến của dự án"
        return f"{project.name} được gợi ý dựa trên {reason}."

    if labels:
        reason = ", ".join(labels)
        return (
            f"{project.name} phù hợp với hồ sơ {risk_tier} của bạn nhờ {reason}. "
            "Đây là giải thích tham khảo, không phải cam kết lợi nhuận."
        )

    return (
        f"{project.name} được xếp hạng cao bởi mô hình gợi ý cho hồ sơ {risk_tier}. "
        "Đây là giải thích tham khảo, không phải cam kết lợi nhuận."
    )


def _json_safe_value(value):
    if value is None:
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    try:
        return round(float(value), 4)
    except (TypeError, ValueError):
        return str(value)
