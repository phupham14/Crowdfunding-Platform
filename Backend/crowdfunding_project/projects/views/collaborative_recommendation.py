import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import projects
from transactions.models import Transaction
from projects.models import Project

def collaborative_recommendation(user, top_n=5):
    # Lấy tất cả giao dịch đầu tư thành công
    tx = Transaction.objects.filter(type="INVEST", status="SUCCESS")

    # Tạo user-project matrix
    users = list(set(tx.values_list('user_id', flat=True)))
    projects = list(set(tx.values_list('project_id', flat=True)))

    # Nếu user chưa có giao dịch nào, không thể recommend bằng collaborative filtering
    if user.id not in users:
        return Project.objects.none()

    # Tạo index để map user_id và project_id sang vị trí trong ma trận
    user_index = {u: i for i, u in enumerate(users)}
    project_index = {p: i for i, p in enumerate(projects)}

    matrix = np.zeros((len(users), len(projects)))

    # Điền ma trận với số tiền đã đầu tư (hoặc 1 nếu không có thông tin số tiền)
    for t in tx:
        if t.project_id:
            matrix[user_index[t.user_id], project_index[t.project_id]] = t.amount or 1

    # Tính cosine similarity giữa user hiện tại và tất cả user khác
    user_vec = matrix[user_index[user.id]].reshape(1, -1)
    similarity = cosine_similarity(user_vec, matrix)[0]

    scores = {}

    # Tính điểm cho các project dựa trên similarity và số tiền đã đầu tư của các user khác
    for i, sim in enumerate(similarity):
        if users[i] == user.id or sim <= 0:
            continue

        for j, invested_amount in enumerate(matrix[i]):
            if invested_amount > 0 and matrix[user_index[user.id], j] == 0:
                scores[projects[j]] = scores.get(projects[j], 0) + sim * invested_amount
    
    print("Users:", users)
    print("Projects:", projects)
    print("Matrix:\n", matrix)
    print("Similarity:", similarity)
    print("Scores:", scores)

    # Lấy top N project có điểm cao nhất
    recommended_project_ids = sorted(scores, key=scores.get, reverse=True)[:top_n]
    return Project.objects.filter(id__in=recommended_project_ids)