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


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category", "location"]
    ordering_fields = ["funding_target", "created_at"]

    def get_permissions(self):
        """
        Quyền theo action:
        - create/update/destroy/change_status: ProjectOwner
        - list/retrieve: public
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'change_status']:
            return [IsAuthenticated(), IsProjectOwner()]
        elif self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

        user = self.request.user

        # Admin → xem tất cả
        if user.is_authenticated and user.role == "ADMIN":
            return project

        # Project owner → xem project của mình (mọi trạng thái)
        if user.is_authenticated and project.owner == user:
            return project

        # Public → chỉ xem OPEN
        if project.status == 'OPEN':
            return project

        # Còn lại → cấm
        raise PermissionDenied("Bạn không có quyền xem project này")

    def get_queryset(self):
        qs = Project.objects.all()

        if self.action == 'list':
            return qs.filter(status='OPEN')

        return qs


    def perform_create(self, serializer):
        # Tự động gán owner khi tạo project
        serializer.save(
            owner=self.request.user,
            status="PENDING"
        )

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
