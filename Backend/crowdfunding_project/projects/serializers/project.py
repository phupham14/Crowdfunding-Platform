from rest_framework import serializers
from ..models import Project

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)
    
    class Meta:
        model = Project
        # Không expose field owner cho client
        fields = [
            "id",
            "owner_name",
            "name",
            "category",
            "description",
            "location",
            "funding_target",
            "apr_expected",
            "start_at",
            "end_at",
            "status",
            "risk_level",
            "expected_return_score",
            "liquidity_score",
            "min_invest_amount",
            "max_invest_amount",
            "min_invest_duration_months",
            "created_at",
            "updated_at",
            "raised",
        ]
        read_only_fields = ["id", "owner_name", "created_at", "updated_at"]
