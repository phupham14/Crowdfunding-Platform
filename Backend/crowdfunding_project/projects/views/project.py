from django.db.models import Q
from interactions.models import UserInteraction
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import rest_framework.status as drf_status

from accounts.permission import IsAdmin, IsInvestor, IsProjectOwner
from projects.models import Project
from projects.serializers.project import ProjectSerializer
from projects.services.recommendation_service import get_recommendation_result
from projects.views.project_permission import ProjectPermission
from risk_profiles.views.risk_evaluation import calculate_all_scores, map_risk_level


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category", "location"]
    ordering_fields = ["funding_target", "created_at"]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role == "ADMIN":
            return Project.objects.all()

        if self.action == "list":
            return Project.objects.filter(status="OPEN")

        if self.action == "retrieve":
            return Project.objects.exclude(status="REJECTED")

        return Project.objects.filter(status="OPEN")

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user, status="PENDING")
        scores = calculate_all_scores(project)

        project.expected_return_score = scores["expected_return_score"]
        project.liquidity_score = scores["liquidity_score"]
        project.risk_level = map_risk_level(scores["risk_score"])
        project.save(update_fields=[
            "expected_return_score",
            "liquidity_score",
            "risk_level",
        ])

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()

        if request.user.is_authenticated:
            UserInteraction.objects.create(
                user=request.user,
                project=project,
                interaction_type="view",
                source="detail_page",
            )
            UserInteraction.objects.create(
                user=request.user,
                project=project,
                interaction_type="click",
                source="detail_page",
            )

        serializer = self.get_serializer(project)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsInvestor, IsAuthenticated], url_path="recommendations")
    def recommendations(self, request):
        top_n = int(request.query_params.get("top_n", 6))
        candidate_limit = int(request.query_params.get("candidate_limit", 100))
        include_explanations = request.query_params.get("explain", "true").lower() not in [
            "0",
            "false",
            "no",
        ]
        result = get_recommendation_result(
            user=request.user,
            top_n=top_n,
            candidate_limit=candidate_limit,
            include_explanations=include_explanations,
        )

        if result.get("error"):
            return Response(
                {"detail": result["error"]},
                status=result.get("status_code", drf_status.HTTP_400_BAD_REQUEST),
            )

        projects = result.pop("recommended_projects")
        explanations = result.pop("explanations", {})
        serialized_projects = self.get_serializer(projects, many=True).data
        if include_explanations:
            for project_data in serialized_projects:
                project_data["explanation"] = explanations.get(project_data["id"])

        result["recommended_projects"] = serialized_projects
        return Response(result)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAdmin], url_path="change-status")
    def change_status(self, request, pk=None):
        project = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["OPEN", "FUNDED", "REPAYING", "COMPLETED", "CANCELLED"]:
            return Response(
                {"error": "Invalid status"},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        project.status = new_status
        project.save()
        return Response({"id": project.id, "status": project.status})

    @action(detail=False, methods=["get"], permission_classes=[], url_path="popular")
    def popular(self, request):
        top_n = int(request.query_params.get("top_n", 6))
        projects = Project.objects.filter(status="OPEN").order_by("-raised")[:top_n]
        serializer = self.get_serializer(projects, many=True)
        return Response({"recommended_projects": serializer.data})

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated, IsProjectOwner],
        url_path="my-projects",
    )
    def my_projects(self, request):
        projects = Project.objects.filter(owner=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
