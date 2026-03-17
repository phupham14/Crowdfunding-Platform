from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.project import ProjectViewSet
from .views.recommendation import ProjectRecommendationAPIView

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = [
    path("recommendations/", ProjectRecommendationAPIView.as_view(), name="project-recommendations"),
    path('', include(router.urls))
]
