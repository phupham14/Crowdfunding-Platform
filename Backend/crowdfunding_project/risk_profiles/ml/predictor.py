import os
import joblib
import numpy as np
from django.conf import settings
from risk_profiles.domain.feature_engineering import compute_engineered_features
from risk_profiles.domain.feature_schema import FEATURE_ORDER

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "risk_profiles/ml/xgboost_model.pkl"
)

model = joblib.load(MODEL_PATH)

def predict_base_score(user_input: dict) -> float:
    """
    user_input: dữ liệu user gửi từ API / frontend
    return: base_score (0–100)
    """

    print("USER INPUT:", user_input)
    print("ENGINEERED FEATURES:")
    features = compute_engineered_features(user_input)

    X = np.array([
        [features[f] for f in FEATURE_ORDER]
    ])
    print("FEATURE VECTOR:", X)

    score = model.predict(X)[0]
    return round(float(score), 2)
