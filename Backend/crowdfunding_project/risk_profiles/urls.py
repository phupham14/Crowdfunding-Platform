# risk_profiles/urls.py
from django.urls import path
from .views.my_profile import MyRiskProfileAPIView
from .views.calculate import CalculateRiskProfileAPIView
from .views.confirm import ConfirmRiskProfileAPIView

urlpatterns = [
    path("me/", MyRiskProfileAPIView.as_view()),
    path("calculate/", CalculateRiskProfileAPIView.as_view()),
    path("confirm/", ConfirmRiskProfileAPIView.as_view()),
]
