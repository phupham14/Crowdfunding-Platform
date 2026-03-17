# projects/serializers.py
from rest_framework import serializers
from projects.models import Project

class ProjectRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "category", "risk_level", "apr_expected", "expected_return_score", "liquidity_score"]
