from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from django.shortcuts import render
from accounts.models.user import User
from transactions.models import Transaction
from projects.models import Project
from adminpanel.serializers import AdminUserSerializer, AdminProjectSerializer, AdminTransactionSerializer
from accounts.permission import IsAdmin
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Sum
from rest_framework.filters import OrderingFilter
from .common.pagination import AdminPageNumberPagination
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_dashboard(request):

    total_users = User.objects.count()

    total_investment = Transaction.objects.filter(
        type="INVEST",
        status="SUCCESS"
    ).aggregate(total=Sum("amount"))["total"] or 0

    pending_projects = Project.objects.filter(status="PENDING").count()

    return Response({
        "total_users": total_users,
        "total_investment": total_investment,
        "pending_projects": pending_projects
    })

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdmin]
    pagination_class = AdminPageNumberPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    # filter theo field
    filterset_fields = ['role', 'is_active']

    # search theo text
    search_fields = ['email', 'full_name']

    def get_queryset(self):
        qs = super().get_queryset()

        locked_param = self.request.query_params.get("locked")

        if locked_param == "true":
            qs = qs.filter(is_active=False)
        elif locked_param == "false":
            qs = qs.filter(is_active=True)

        return qs

    # POST /admin/users/<id>/block/
    @action(detail=True, methods=['post'], url_path='block')
    def lock(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"Message": "Account blocked"})

    # POST /admin/users/<id>/unblock/
    @action(detail=True, methods=['post'], url_path='unblock')
    def unlock(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"Message": "Account unblocked"})
    
    # POST /admin/users/<id>/verify/
    @action(detail=True, methods=["post"], url_path="verify")
    def verify(self, request, pk=None):
        """Duyệt tài khoản chủ dự án"""
        user = self.get_object()
        user.is_verified = True # Chủ dự án đã được duyệt
        user.role = "PROJECT_OWNER"
        user.save()
        return Response({"status": "User verified"}, status=status.HTTP_200_OK)

class AdminProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('id')
    serializer_class = AdminProjectSerializer
    permission_classes = [IsAdmin]
    pagination_class = AdminPageNumberPagination
    http_method_names = ['get', 'post']

    def get_queryset(self):
        qs = super().get_queryset()

        status_param = self.request.query_params.get('status')
        type_param = self.request.query_params.get('type')

        if status_param:
            qs = qs.filter(status=status_param)
        if type_param:
            qs = qs.filter(type=type_param)

        return qs
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        project = self.get_object()
        project.status = 'OPEN'
        project.save(update_fields=['status'])
        return Response({'message': 'Project approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin], url_path='reject')
    def reject(self, request, pk=None):
        project = self.get_object()

        # Chỉ set status = REJECTED, không cần data
        project.status = "REJECTED"
        project.save()

        return Response({"id": project.id, "status": project.status})


class AdminTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all().order_by("-created_at")
    serializer_class = AdminTransactionSerializer
    permission_classes = [IsAdmin]
    pagination_class = AdminPageNumberPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'amount', 'created_at']
    ordering = ['id']

    def get_queryset(self):
        qs = super().get_queryset()

        status_param = self.request.query_params.get('status')
        type_param = self.request.query_params.get('type')

        if status_param:
            qs = qs.filter(status=status_param)

        if type_param:
            qs = qs.filter(type=type_param)

        return qs

class SystemReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "total_users": User.objects.count(),
            "total_projects": Project.objects.count(),
            "total_transactions": Transaction.objects.count(),
            "total_money_flow": Transaction.objects.filter(
                status="SUCCESS"
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        })
