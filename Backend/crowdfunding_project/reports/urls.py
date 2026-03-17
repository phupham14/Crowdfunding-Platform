from django.urls import path
from reports.views.portfolio_report import PortfolioReportAPIView
from reports.views.revenue_report import RevenueReportAPIView

urlpatterns = [
    path("portfolio/", PortfolioReportAPIView.as_view()),
    path("revenue/", RevenueReportAPIView.as_view()),
]
