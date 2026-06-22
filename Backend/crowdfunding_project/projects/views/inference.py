import joblib
import pandas as pd
import numpy as np

def prepare_inference_data(user_profile, candidates_list, stats):
    """
    user_profile: Dict chứa thông tin user từ DB
    candidates_list: Danh sách Dict/Objects các project từ DB (Top Popularity)
    stats: Các thông số trung bình đã lưu (user_avg_apr, etc.)
    """
    # Chuyển candidates sang DataFrame để xử lý hàng loạt
    df_cand = pd.DataFrame(candidates_list)

    # Gán thông tin user vào từng dòng candidate
    for key, value in user_profile.items():
        df_cand[key] = value

    # Tái hiện Feature Engineering (Copy từ hàm add_features lúc train)
    df_cand['user_avg_apr'] = stats.get('user_avg_apr', 13.0) # Fallback value
    df_cand['user_avg_risk'] = stats.get('user_avg_risk', 2.5)

    df_cand['log_income'] = np.log1p(df_cand['income'])
    df_cand['log_apr'] = np.log1p(df_cand['apr_expected'])

    df_cand['risk_gap'] = abs(df_cand['risk_pref'] - df_cand['risk_level'])
    df_cand['apr_diff'] = df_cand['apr_expected'] - df_cand['user_avg_apr']

    df_cand['apr_ratio'] = df_cand['apr_expected'] / (df_cand['user_avg_apr'] + 1e-5)
    df_cand['return_per_risk'] = df_cand['apr_expected'] / (df_cand['risk_level'] + 1e-5)

    # Các cột khác như 'view' hay 'click' lúc inference có thể mặc định là 0 hoặc 1 tùy logic
    df_cand['view'] = 1
    df_cand['click'] = 0

    return df_cand