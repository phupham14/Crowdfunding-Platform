from django.urls import path
from transactions.views.fundin import FundInAPIView
from transactions.views.withdraw import WithdrawAPIView
from transactions.views.history import TransactionHistoryAPIView
from transactions.views.investment import ProjectInvestmentAPIView

urlpatterns = [
    path("fund-in/", FundInAPIView.as_view(), name="fund-in"),
    path("withdraw/", WithdrawAPIView.as_view(), name="withdraw"),
    path("history/", TransactionHistoryAPIView.as_view(), name="transaction-history"),
    path("projects/<int:project_id>/invest/", ProjectInvestmentAPIView.as_view()),
]