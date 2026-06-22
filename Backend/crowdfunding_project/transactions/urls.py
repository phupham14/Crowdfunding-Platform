from django.urls import path
from transactions.views.fundin import FundInAPIView
from transactions.views.fundout import FundOutAPIView
from transactions.views.history import TransactionHistoryAPIView
from transactions.views.investment import ProjectInvestmentAPIView
from transactions.views.project_owner_cashflow import (
    ProjectDisbursementAPIView,
    ProjectRepaymentAPIView,
)
from transactions.views.webhook import stripe_webhook
from transactions.views.confirm_payment import confirm_payment

urlpatterns = [
    path("fund-in/", FundInAPIView.as_view(), name="fund-in"),
    path("fund-out/", FundOutAPIView.as_view(), name="fund-out"),
    path("history/", TransactionHistoryAPIView.as_view(), name="transaction-history"),
    path("projects/<int:project_id>/invest/", ProjectInvestmentAPIView.as_view()),
    path("projects/<int:project_id>/disburse/", ProjectDisbursementAPIView.as_view()),
    path("projects/<int:project_id>/repay/", ProjectRepaymentAPIView.as_view()),
    path("webhook/", stripe_webhook),
    path("confirm-payment/", confirm_payment),
]
