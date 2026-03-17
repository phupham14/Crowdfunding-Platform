from rest_framework.views import APIView
from accounts.permission import IsInvestor
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from projects.models import Project
from risk_profiles.models import RiskProfile
from projects.serializers.recommendation import ProjectRecommendationSerializer
from risk_profiles.services import get_risk_tier, get_allowed_project_risk_levels
from transactions.models import Transaction
from projects.views.collaborative_recommendation import collaborative_recommendation


class ProjectRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInvestor]

    def get(self, request):
        user = request.user
        TOP_N = 5

        # ===== Risk profile =====
        risk_profile = RiskProfile.objects.filter(user=user).first()
        if not risk_profile:
            return Response(
                {"detail": "Please complete risk profiling first"},
                status=400
            )

        risk_tier = get_risk_tier(risk_profile.base_score)
        allowed_risk_levels = get_allowed_project_risk_levels(risk_tier)

        # ===== Base queryset (fallback pool) =====
        base_qs = Project.objects.filter(
            status="OPEN",
            risk_level__in=allowed_risk_levels
        )

        # ===== Check history =====
        has_transactions = Transaction.objects.filter(
            user=user,
            type="INVEST",
            status="SUCCESS"
        ).exists()

        if has_transactions:
            # Collaborative filtering
            cf_qs = collaborative_recommendation(user)

            # Filter theo business rule
            cf_qs = cf_qs.filter(
                status="OPEN",
                risk_level__in=allowed_risk_levels
            )

            # Lấy danh sách ID
            cf_ids = list(cf_qs.values_list("id", flat=True))

            # Nếu đủ thì cắt TOP_N luôn
            if len(cf_ids) >= TOP_N:
                final_qs = cf_qs[:TOP_N]

            else:
                # fallback bổ sung cho đủ TOP_N
                remaining_needed = TOP_N - len(cf_ids)

                fallback_qs = base_qs.exclude(id__in=cf_ids)[:remaining_needed]

                final_qs = list(cf_qs) + list(fallback_qs)

        else:
            # Cold start
            final_qs = base_qs[:TOP_N]

        print("Recommended project IDs:", [p.id for p in final_qs])
        print("After filtering, risk levels:", [p.risk_level for p in final_qs])

        # ===== Serialize =====
        serializer = ProjectRecommendationSerializer(
            final_qs,
            many=True
        )

        return Response({
            "risk_tier": risk_tier,
            "recommended_projects": serializer.data
        })