# risk_profiles/views.py
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.permission import IsInvestor
from risk_profiles.models import RiskProfile
from risk_profiles.serializers.serializers import RiskProfileSerializer

class MyRiskProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsInvestor]
    serializer_class = RiskProfileSerializer

    def get_object(self):
        profile, _ = RiskProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile
