"""
URL configuration for crowdfunding_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),  # Django admin UI
    path("api/accounts/", include("accounts.urls")),  # REST API for accounts
    path("api/projects/", include("projects.urls")),  # REST API for projects
    path("api/transactions/", include("transactions.urls")),  # REST API for transactions
    path("api/reports/", include("reports.urls")),  # REST API for reports
    path("api/admin/", include("adminpanel.urls")),  # REST API for admin
    path("api/risk-profiles/", include("risk_profiles.urls")),  # REST API for risk profiles
]
