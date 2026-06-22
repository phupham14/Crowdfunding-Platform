from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.project_owner_application import ProjectOwnerApplication
from accounts.permission import IsAdmin
from accounts.serializers.project_owner_application import (
    ProjectOwnerApplicationReviewSerializer,
    ProjectOwnerApplicationSerializer,
)
from accounts.services.project_owner_application_service import (
    approve_project_owner_application,
    reject_project_owner_application,
    submit_project_owner_application,
)


class MyProjectOwnerApplicationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            application = request.user.project_owner_application
        except ProjectOwnerApplication.DoesNotExist:
            return Response({"detail": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectOwnerApplicationSerializer(application)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "INVESTOR":
            return Response(
                {"detail": "Only investors can submit project owner applications"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProjectOwnerApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        application, created = submit_project_owner_application(request.user, serializer.validated_data)
        response_serializer = ProjectOwnerApplicationSerializer(application)
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(response_serializer.data, status=response_status)


class ProjectOwnerApplicationListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        applications = ProjectOwnerApplication.objects.select_related("user", "reviewed_by").order_by("-created_at")
        serializer = ProjectOwnerApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class ProjectOwnerApplicationApproveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            application = ProjectOwnerApplication.objects.select_related("user").get(pk=pk)
        except ProjectOwnerApplication.DoesNotExist:
            return Response({"detail": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        application = approve_project_owner_application(application, request.user)
        serializer = ProjectOwnerApplicationSerializer(application)
        
        return Response(serializer.data)


class ProjectOwnerApplicationRejectAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            application = ProjectOwnerApplication.objects.select_related("user").get(pk=pk)
        except ProjectOwnerApplication.DoesNotExist:
            return Response({"detail": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectOwnerApplicationReviewSerializer(
            data=request.data,
            context={"action": "reject"},
        )
        serializer.is_valid(raise_exception=True)

        application = reject_project_owner_application(
            application,
            request.user,
            serializer.validated_data["reject_reason"],
        )
        response_serializer = ProjectOwnerApplicationSerializer(application)
        return Response(response_serializer.data)
