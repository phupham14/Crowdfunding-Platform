from openai import project

from interactions.models import UserInteraction
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
import rest_framework.status as drf_status
from django.http import Http404
from django.core.exceptions import PermissionDenied

from projects.models import Project
from projects.serializers.project import ProjectSerializer
from accounts.permission import IsProjectOwner
from risk_profiles.views.risk_evaluation import calculate_all_scores, map_risk_level
from django.db.models import Q


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category", "location"]
    ordering_fields = ["funding_target", "created_at"]

    # Permission: anyone can view, only authenticated can create/update
    def get_queryset(self):
        user = self.request.user

        # Admin → thấy tất cả
        if user.is_authenticated and user.role == "ADMIN":
            return Project.objects.all()

        # User → thấy project của mình + project OPEN
        if user.is_authenticated:
            return Project.objects.filter(
                Q(owner=user) | Q(status="OPEN")
            )

        # Public → chỉ OPEN
        return Project.objects.filter(status="OPEN")

    # Override create để tính score khi tạo project
    def perform_create(self, serializer):
        project = serializer.save(
            owner=self.request.user,
            status="PENDING"
        )

        scores = calculate_all_scores(project)

        project.expected_return_score = scores["expected_return_score"]
        project.liquidity_score = scores["liquidity_score"]
        risk_score = scores["risk_score"]
        project.risk_level = map_risk_level(risk_score)

        project.save(update_fields=[
            "expected_return_score",
            "liquidity_score",  
            "risk_level"
        ])

    # Override retrieve để log interaction
    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()

        if request.user.is_authenticated:
            UserInteraction.objects.create(
                user=request.user,
                project=project,
                interaction_type="view",
                source="detail_page"
            )

            UserInteraction.objects.create(
                user=request.user,
                project=project,
                interaction_type="click",
                source="detail_page"
            )

        serializer = self.get_serializer(project)
        return Response(serializer.data)

    # Chỉ project owner mới được đổi status
    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        project = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ["OPEN", "CLOSED", "CANCELLED"]:
            return Response({"error": "Invalid status"}, status=drf_status.HTTP_400_BAD_REQUEST)

        project.status = new_status
        project.save()
        return Response({"id": project.id, "status": project.status})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsProjectOwner], url_path='my-projects')
    def my_projects(self, request):
        projects = Project.objects.filter(owner=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
