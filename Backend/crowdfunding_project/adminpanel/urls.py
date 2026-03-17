from rest_framework import routers
from adminpanel.views import (
    AdminUserViewSet, AdminProjectViewSet, 
    AdminTransactionViewSet, SystemReportView,
    admin_dashboard
)
from django.urls import path

from .views import (
    AdminUserViewSet,
    AdminProjectViewSet,
    AdminTransactionViewSet,
    SystemReportView,
    admin_dashboard
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("users", AdminUserViewSet, basename="admin-users")
router.register("projects", AdminProjectViewSet, basename="admin-projects")
router.register("transactions", AdminTransactionViewSet, basename="admin-transactions")

urlpatterns = [
    # Reports
    path("system-report/", SystemReportView.as_view(), name="admin-report"),
    path("dashboard/", admin_dashboard, name="admin-dashboard"),
]

urlpatterns += router.urls
